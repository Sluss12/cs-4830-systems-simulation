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
    def __init__(self, customerNo, resources):
        self.env = resources.env
        self.customerNo = customerNo
        self.orderStationLine = resources.orderStationLine
        self.orderStation = resources.orderStation
        self.orderStationNo = -1
        self.paymentLine = resources.paymentLine
        self.paymentWindow = resources.paymentWindow
        self.pickupLine = resources.pickupLine
        self.pickupWindow = resources.pickupWindow
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
        print(f'Customer {self.customerNo} has arrived at {self.env.now:.2f}.')
        # check if line is full
        maxLineSize = 8
        if len(self.orderStationLine.queue) >= maxLineSize: # Max cars waiting for order station is 8
            lostCustomerList.append(1.0)
            return # Bawk
        # get in line
        getInOrderStationLine = self.orderStationLine.request()
        yield getInOrderStationLine # at the front of order line
        print(f'Customer {self.customerNo} got to front of order station line at {self.env.now:.2f}.')
        # pick order station
        if self.orderStation[0].count < self.orderStation[0].capacity: # station 0 empty
            self.orderStationNo = 0
        elif self.orderStation[1].count < self.orderStation[1].capacity: # station 1 empty
            self.orderStationNo = 1
        elif len(self.orderStation[0].queue) < len(self.orderStation[1].queue): #neither station is empty, pick the shortest queue
            self.orderStationNo = 0
        else:
            self.orderStationNo = 1
        # order station
        requestOrderStation = self.orderStation[self.orderStationNo].request() # wait for specific orderstation
        yield requestOrderStation
        print(f'Customer {self.customerNo} got to order station {self.orderStationNo} at {self.env.now:.2f}.')
        yield self.orderStationLine.release(getInOrderStationLine) # out of line, at order station
        self.timeOfOrder = self.env.now
        yield self.env.timeout(self.timeToOrder)
        print(f'Customer {self.customerNo} finished at order station {self.orderStationNo} at {self.env.now:.2f}.')
        # payment line
        getInPaymentLine = self.paymentLine.request() # wait for payment line
        yield getInPaymentLine
        print(f'Customer {self.customerNo} got in payment line at {self.env.now:.2f}.')
        yield self.orderStation[self.orderStationNo].release(requestOrderStation) # out of order station, in line
        # payment window
        requestPaymentWindow = self.paymentWindow.request() # wait for payment window
        yield requestPaymentWindow
        print(f'Customer {self.customerNo} got to payment window at {self.env.now:.2f}.')
        yield self.paymentLine.release(getInPaymentLine) # out of line, at payment window
        self.timeOfPayment = self.env.now
        yield self.env.timeout(self.timeToPay)
        # pickup line
        getInPickupLine = self.pickupLine.request() # wait for pickup line
        yield getInPickupLine
        print(f'Customer {self.customerNo} got in pickup line at {self.env.now:.2f}.')
        yield self.paymentWindow.release(requestPaymentWindow) # out of payment window, in line
        # pickup window
        requestPickWindow = self.pickupWindow.request() # wait for pickup window
        yield requestPickWindow
        yield self.pickupLine.release(getInPickupLine) # out of line, at pickup window
        self.timeOfPickup = self.env.now
        print(f'Customer {self.customerNo} got to pickup window at {self.env.now:.2f}.')
        yield self.env.timeout(self.timeToPickup)
        yield self.pickupWindow.release(requestPickWindow) # customer finished, now leaving
        print(f'Customer {self.customerNo} left at {self.env.now:.2f}.')


def customerGenerator(resources):
    customerNo = 1
    while True:
        interarrivalRate = 1.0 #time delay between cust
        yield resources.env.timeout(interarrivalRate)
        customer = Customer(customerNo, resources)
        resources.env.process(customer.orderProcess())
        customerNo += 1
        noCustomersProccessedList.append(1.0)

class simResources:
    def __init__(self,):
        self.env = simpy.Environment()
        self.orderStationLine = simpy.Resource(self.env, capacity=1)
        self.orderStation = [simpy.Resource(self.env, capacity=1), simpy.Resource(self.env, capacity=1)]
        self.paymentLine = simpy.Resource(self.env, capacity=4)
        self.paymentWindow = simpy.Resource(self.env, capacity=1)
        self.pickupLine = simpy.Resource(self.env, capacity=1)
        self.pickupWindow = simpy.Resource(self.env, capacity=1)

averageTotalTimeTaken = []
averageLostCustomers = []
averageCustomersProcessed = []
runs = 1
for replicate in range(runs):
    totalTimeTakenList = []
    lostCustomerList = []
    noCustomersProccessedList = []
    resources = simResources()
    resources.env.process(customerGenerator(resources))
    resources.env.run(until=30.0)
    averageTotalTimeTaken.append(np.average(totalTimeTakenList))
    averageLostCustomers.append(np.sum(lostCustomerList))
    averageCustomersProcessed.append(np.sum(noCustomersProccessedList)-np.sum(lostCustomerList))
