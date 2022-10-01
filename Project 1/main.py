# -*- coding: utf-8 -*-
"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 1
@description: For this project we are simulating two different drive-thru scenarios. This drive-thru simulation consists of a pair of order stations and payment/pickup window, as space is limited our goal is to optimize throughput of cars to maximize profit during the lunch rush that occurs from 11am - 1pm, or over a 2 hour window.
"""
#%% cell to view graphs

# list of resources
from scipy import rand
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

def print_stats(res, who):
    print(f'user: {who}')
    print(f'{res.count} of {res.capacity} slots are allocated.')
    print(f'  Users: {res.users}')
    print(f'  Queued events: {res.queue}')
class Customer:
    def __init__(self, number, env, line, orderStations, kitchen, pickupLine, pickupWindow):
        self.customerNo = number
        self.env = env
        self.line = line
        self.orderStations = orderStations
        self.kitchen = kitchen
        self.pickupLine = pickupLine
        self.pickupWindow = pickupWindow
        self.timeToOrder = random.expovariate(1/2.5)
        self.timeToPrepFood = random.expovariate(1/5.0)
        self.timeToPay = random.expovariate(1/2.0)
        self.lineNo = 0
        self.timeOfArrival = 0
        self.timeOfOrder = 0
        self.timeOfPayment = 0
        self.timeOfFoodReady = 0
        self.remainingPrepTime = 0

    def printOrderSummary(self):
        print(f'Customer Number: {self.customerNo}')
        print(f'Line Number: {self.lineNo}')
        print(f'Time of Order: {self.timeOfOrder:.3f}')
        print(f'Time to Order: {self.timeToOrder:.3f}')
        print(f'Prep Time: {self.timeToPrepFood:.3f}')
        print(f'Remaining Prep Time: {self.remainingPrepTime:.3f}')
        print(f'Time of Payment: {self.timeOfPayment:.3f}')
        print(f'Time to Pay: {self.timeToPay:.3f}')
        print(f'Wait Time: {self.customerNo}')
        
    def inLine(self):
        self.timeOfArrival = self.env.now
        print(f'Customer {self.customerNo} has arrived at simTime {self.env.now:.3f}')
        #pick line
        # if either line is below capacity, get in that line
        if self.line[0].count < self.line[0].capacity or self.line[1].count < self.line[1].capacity:
            if self.line[0].count < self.line[1].count:
                self.lineNo = 0
            else:
                self.lineNo = 1
        else:  # bawk
            self.lineNo = 2
        print_stats(self.line[self.lineNo], self.customerNo)
        print(f'Customer {self.customerNo} picked line {self.lineNo}')
        if self.lineNo != 2:
            #get in line
            getInLine = self.line[self.lineNo].request()
            yield getInLine
            #ordering
            getToOrderStation = self.orderStations[self.lineNo].request()
            yield getToOrderStation
            yield self.line[self.lineNo].release(getInLine)
            print(f'Customer {self.customerNo} got to orderStation {self.lineNo} at simTime {self.env.now:.3f}')
            yield self.env.timeout(self.timeToOrder)
            yield self.orderStations[self.lineNo].release(getToOrderStation)
            self.timeOfOrder = self.env.now
            print(f'Customer {self.customerNo} finished at orderStation {self.lineNo} at simTime {self.env.now:.3f}. With an order time of {self.timeToOrder:.3f}, thier food will take {self.timeToPrepFood:.3f} minutes')
            #pickup line
            getInPickupLine = self.pickupLine.request()
            yield getInPickupLine
            #pickup and pay
            print_stats(self.pickupLine,self.customerNo)
            getToPickupWindow = self.pickupWindow.request()
            yield getToPickupWindow
            yield self.pickupLine.release(getInPickupLine)
            print(f'Customer {self.customerNo} got to pickupWindow at simTime {self.env.now:.3f}')
            self.remainingPrepTime = self.timeToPrepFood-(self.env.now - self.timeOfOrder)
            print(f'Remaining Prep Time: {self.remainingPrepTime:.3f}')
            if self.remainingPrepTime > 0.0:
                yield self.env.timeout(self.remainingPrepTime)
            print(f'Customer {self.customerNo} food is ready at simTime {self.env.now:.3f}')
            yield self.env.timeout(self.timeToPay)
            yield self.pickupWindow.release(getToPickupWindow)
            print(f'Customer {self.customerNo} finished paying, got food, and left at simTime {self.env.now:.3f}')
        else:
            print(f'Customer {self.customerNo} has BAWKED on arrival simTime {self.env.now:.3f}')
            

def arrivalProcess(env):
    line = [simpy.Resource(env, capacity=5), simpy.Resource(env, capacity=5),simpy.Resource(env)]
    orderStations = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
    kitchen = simpy.Resource(env)
    pickupLine = simpy.Resource(env, capacity=5)
    pickupWindow = simpy.Resource(env, capacity=1)
    customerNo = 0
    while True:
        interarrivalRate = random.expovariate(1/2.0)
        yield env.timeout(interarrivalRate)  # time delay between cust
        customer = Customer(customerNo, env, line, orderStations, kitchen, pickupLine, pickupWindow)
        env.process(customer.inLine())
        customerNo += 1
        

env = simpy.Environment()
env.process(arrivalProcess(env))
env.run(until=60.0) 

# Watching Lecture on 9/2/22 at timestamp 33:29