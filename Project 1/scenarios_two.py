# -*- coding: utf-8 -*-
"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 1
@description: For this project we are simulating two different drive-thru scenarios. This drive-thru simulation consists of a pair of order stations and payment/pickup window, as space is limited our goal is to optimize throughput of cars to maximize profit during the lunch rush that occurs from 11am - 1pm, or over a 2 hour window.
"""
#%% cell to view graphs

# list of resources
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
    def __init__(self, number, env, line, orderStations, pickupLine, pickupWindow):
        self.customerNo = number
        self.env = env
        self.line = line
        self.orderStations = orderStations
        self.pickupLine = pickupLine
        self.pickupWindow = pickupWindow
        self.timeToOrder = random.expovariate(1/1.5)
        self.timeToPrepFood = random.expovariate(1/5.0)
        self.timeToPay = random.expovariate(1/1.0)
        self.lineNo = 0
        # For Use in Stats
        self.bawk = False
        self.totalDriveThruTime = 0
        self.timeOfArrival = 0
        self.timeOfOrder = 0
        self.timeOfPayment = 0
        self.timeCustomerLeft = 0
        self.timeOfFoodReady = 0
        self.remainingPrepTime = 0
        self.peopleInOrderLineOnArrival= 0
        self.peopleInPickupLineAfterOrdering= 0
        self.peopleWaitingForPickupLine=0

    def print_OrderSummary(self):
        print(f'Customer Number: {self.customerNo}')
        print(f'Line Number: {self.lineNo}')
        print(f'  Time of Arrival: {self.timeOfArrival:.3f}')
        print(f'  Time of Order: {self.timeOfOrder:.3f}')
        print(f'  Prep Time: {self.timeToPrepFood:.3f}')
        print(f'  Time Food is Ready: {self.timeOfFoodReady:.3f}')
        print(f'  Time of Payment: {self.timeOfPayment:.3f}')
        print(f'  Time Customer Left: {self.timeCustomerLeft:.3f}')
        print(f'----\n  Total Drive-Thru Time: {self.timeCustomerLeft-self.timeOfArrival:.3f}\n-----')
        print(f'Time Waiting in Order Line: {self.timeOfOrder-self.timeOfArrival:.3f}')
        print(f'Time to Order: {self.timeToOrder:.3f}')
        print(f'Time Waiting in Payment Line {self.timeOfPayment- self.timeOfOrder:.3f}')
        print(f'Remaining Prep Time at Payment window: {self.remainingPrepTime:.3f}')
        print(f'Time to Pay: {self.timeToPay:.3f}')
        print(f'Number of people ahead in order line: {self.peopleInOrderLineOnArrival}')
        print(f'Number of people waiting to get in pickup line: {self.peopleWaitingForPickupLine}')
        print(f'Number of people ahead in pickup line: {self.peopleInPickupLineAfterOrdering}\n')
    
    def inLine(self):
        self.timeOfArrival = self.env.now
        print(f'Customer {self.customerNo} has arrived at: {self.env.now:.3f}')
        #check if line is full
        if (len(self.line[0].queue) + len(self.line[1].queue)) >= 12:
            print(f'Customer {self.customerNo} HAS BAWKED ON ARRIVAL at simTime {self.env.now:.3f}')
            lostCustomerList.append(1.0)
            return
        #pick line
        if self.line[0].count < self.line[0].capacity:  #line 0 empty case
            self.lineNo = 0
        elif self.line[1].count < self.line[1].capacity: #line 1 empty case
            self.lineNo = 1
        elif len(self.line[0].queue) < len(self.line[1].queue): #neither line is empty, pick the shortest queue
            self.lineNo = 0
        else:
            self.lineNo = 1
        self.peopleInOrderLineOnArrival = len(self.orderStations[self.lineNo].queue) + self.orderStations[self.lineNo].count
        #get in line
        getInOrderLine = self.line[self.lineNo].request()  # get in line
        #get to order station
        getToOrderStation = self.orderStations[self.lineNo].request() #get in line for orderstation
        yield getInOrderLine
        print(f'Customer {self.customerNo} got in line {self.lineNo} at: {self.env.now:.3f}')
        #print(f'  Length of Order Station {self.lineNo} Queue: {len(self.orderStations[self.lineNo].queue)}')
        yield getToOrderStation
        print(f'Customer {self.customerNo} got to ORDERSTATION {self.lineNo} at: {self.env.now:.3f}')
        yield self.env.timeout(self.timeToOrder)
        self.timeOfOrder = self.env.now
        print(f'Customer {self.customerNo} ordered food at: {self.env.now:.3f}')
        self.timeOfFoodReady = self.timeOfOrder + self.timeToPrepFood
        print(f'Customer {self.customerNo} food will be ready at {self.timeOfFoodReady:.3f}')
        self.timeOfPayment = self.env.now
        yield self.env.timeout(self.timeToPay)
        print(f'Customer {self.customerNo} paid for their food at: {self.env.now:.3f}')
        yield self.orderStations[self.lineNo].release(getToOrderStation) #after paying for food release the order station
        #get in pickup line
        self.peopleInPickupLineAfterOrdering = self.pickupLine.count
        self.peopleWaitingForPickupLine = len(self.pickupLine.queue)
        getInPickupLine = self.pickupLine.request()
        print(f'Customer {self.customerNo} is waiting for the pickup line at: {self.env.now:.3f}')
        print(f'  Number of people already in the pickup line: {self.peopleInPickupLineAfterOrdering}')
        print(f'  Number of people waiting for pickup line: {len(self.pickupLine.queue)}')
        yield getInPickupLine
        yield self.line[self.lineNo].release(getInOrderLine) #once there is space in the pickup line, leave the order line
        print(f'Customer {self.customerNo} got in the pickup line at: {self.env.now:.3f}')
        #get to pickup window then wait for food to finish
        getToPickupWindow = self.pickupWindow.request()
        yield getToPickupWindow
        yield self.pickupLine.release(getInPickupLine) #once there is space at the checkout window, leave the pickup line
        print(f'Customer {self.customerNo} got out of the pickup line and to the window at: {self.env.now:.3f}')
        self.remainingPrepTime = self.timeToPrepFood-(self.env.now - self.timeOfOrder)
        if self.remainingPrepTime > 0.0:
            print(f'Customer {self.customerNo} food will be ready in: {self.remainingPrepTime:.3f} more min')
            yield self.env.timeout(self.remainingPrepTime)
            print(f'Customer {self.customerNo} food is ready at: {self.env.now:.3f}')
        else:
            print(f'Customer {self.customerNo} food was ready: {-1 * self.remainingPrepTime:.3f} min ago')
        #payment
        yield self.pickupWindow.release(getToPickupWindow)
        print(f'Customer {self.customerNo} picked up food and left at: {self.env.now:.3f}')
        self.timeCustomerLeft = self.env.now
        self.totalDriveThruTime = self.timeCustomerLeft - self.timeOfArrival
        totalTimeTakenList.append(self.totalDriveThruTime)
        #self.print_OrderSummary()

def customerGenerator(env,line, orderStations, pickupLine, pickupWindow):
    customerNo = 1
    while True:
        interarrivalRate = random.expovariate(1/meanInterArrivalTime) #time delay between cust
        yield env.timeout(interarrivalRate)  
        customer = Customer(customerNo, env, line, orderStations, pickupLine, pickupWindow)
        env.process(customer.inLine())
        customerNo += 1

meanInterArrivalTime = 2.0
averageTotalTimeTaken = []
averageLostCustomers = []
for replicate in range(10000):
    totalTimeTakenList = []
    lostCustomerList = []
    env = simpy.Environment()
    line = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
    orderStations = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
    pickupLine = simpy.Resource(env, capacity=6)
    pickupWindow = simpy.Resource(env, capacity=1)
    env.process(customerGenerator(env,line,orderStations,pickupLine,pickupWindow))
    env.run(until=120.0) 
    averageTotalTimeTaken.append(np.average(totalTimeTakenList))
    averageLostCustomers.append(np.sum(lostCustomerList))
    
print(averageTotalTimeTaken)
print(averageLostCustomers)
print(f'The mean interarrival time of customers is: {meanInterArrivalTime}')
print(f'The drive-thru simulation ran for 120 time units, to simulate the lunch rush from 11:00am to 1:00pm.')
print(f'The average total time taken over 10000 runs is {np.average(averageTotalTimeTaken):0.3f}')
print(f'The average number of customers to bawk over 100 runs is {np.average(averageLostCustomers):0.3f}')

plt.figure()
plt.hist(averageLostCustomers, bins=10)
plt.xlabel('average number of customers lost')
plt.ylabel('frequency')
plt.title('Customers Lost over 100 Runs')
plt.show()

# %%
