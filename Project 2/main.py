"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 2
@description: For our second project, we will study how to model and simulate input distributions. Since we have simple queuing simulation experience, we will use the McDonald’s restaurant across the street from Wright State as our source of data. 
"""
#%% cell to view graphs

# list of resources
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

class Customer:
    def __init__(self, env, number,orderStationLine, orderStations, pickupLine, pickupWindow):
        self.env = env
        self.customerNo = number
        self.orderStationLine = orderStationLine
        self.orderStations = orderStations
        self.orderStationNo = -1
        self.pickupLine = pickupLine
        self.pickupWindow = pickupWindow
        self.timeToOrder = 5.0
        self.timeToPay = 3.0
        self.timeToPickup = 2.0
        # For Use in Stats
        self.bawk = False
        self.totalDriveThruTime = -1
        self.timeOfArrival = -1
        self.timeOfOrder = -1
        self.timeOfPayment = -1
        self.timeOfPickup = -1
        self.timeCustomerLeft = 0

    def orderProcess(self):
        self.timeOfArrival = self.env.now
        # check if line is full
        if len(self.orderStationLine.queue) >= 8: # Max cars waiting for order station is 8
            lostCustomerList.append(1.0)
            return # Bawk
        # get in line
        getInOrderStationLine = self.orderStationLine.request()
        yield getInOrderStationLine # at the front of order line
        # pick order station
        if self.orderStations[0].count < self.orderStations[0].capacity:
            self.orderStationNo = 0
        elif self.orderStations[1].count < self.orderStations[1].capacity:
            self.orderStationNo = 1
        elif len(self.orderStations)
        getToOrderStation = self.orderStations[self.orderStationNo].request() # get in line for specific orderstation
        # get to order station
        
        # get in payment line
        
        # payment window
        
        # pickup line
        
        # pickup window
        

def customerGenerator(env, orderStations, pickupLine, pickupWindow):
    customerNo = 1
    while True:
        interarrivalRate = 0.5 #time delay between cust
        yield env.timeout(interarrivalRate)  
        customer = Customer(env, customerNo, orderStationLine, orderStations, pickupLine, pickupWindow)
        env.process(customer.orderProcess())
        customerNo += 1
        noCustomersProccessedList.append(1.0)


averageTotalTimeTaken = []
averageLostCustomers = []
averageCustomersProcessed = []
runs = 1000
for replicate in range(runs):
    totalTimeTakenList = []
    lostCustomerList = []
    noCustomersProccessedList = []
    env = simpy.Environment()
    orderStationLine = simpy.Resource(env, capacity=1)
    orderStations = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
    pickupLine = simpy.Resource(env, capacity=6)
    pickupWindow = simpy.Resource(env, capacity=1)
    env.process(customerGenerator(env,orderStations,pickupLine,pickupWindow))
    env.run(until=120.0) 
    averageTotalTimeTaken.append(np.average(totalTimeTakenList))
    averageLostCustomers.append(np.sum(lostCustomerList))
    averageCustomersProcessed.append(np.sum(noCustomersProccessedList)-np.sum(lostCustomerList))
