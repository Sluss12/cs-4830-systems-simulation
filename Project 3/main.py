"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 3
@description: For our second project, we will study the elevators of the Russ engineering building.
@file_name: main.py
@file_description: main.py is the main driver for the simulation which makes all simulation calls, and contains the logical pertaining to the process and order of simulation events. main.py also handles analysis of the simulation results.
"""
#%% cell to view graphs

# list of resources
import os
from tkinter import Y
import simpy
import random
import numpy as np

#%%
class simResources:
    def __init__(self):
        self.env = simpy.Environment()
        self.elevators = [simpy.Resource(self.env, capacity=1),
                          simpy.Resource(self.env, capacity=1)]
        self.elevatorPosition = [0,0]
        self.callButton = [simpy.Resource(self.env, capacity=1),
                           simpy.Resource(self.env, capacity=1),
                           simpy.Resource(self.env, capacity=1),
                           simpy.Resource(self.env, capacity=1)]
        self.travelTimes = [0.0, 2.0, 4.0, 6.0, 8.0]

#%%
class defaultRider:
    def __init__(self, riderNo, resources):
        self.riderNo = riderNo
        self.resources = resources
        self.timeForElevatorToArrive = 1
        self.timeForDoorsToOpenOrClose = 1
        self.timeForElevatorToTravel = 1
        self.elevatorNo = -1
        self.riderStartFloor = -1
        self.riderEndFloor = -1
        # For Use in Stats
        self.timeOfRiderArrival = -1
        self.timeOfElevatorArrival = -1

    def rideElevator(self):
        self.timeOfRiderArrival = self.env.now
        self.riderStartFloor = self.pickRiderFloor()
        self.riderEndFloor = self.pickDestinationFloor()
        print(f'Rider {self.riderNo} has arrived at {self.env.now:.2f} on floor {self.riderStartFloor}')
        self.elevatorNo = self.pickServiceingElevator()
        elevatorMoving = self.resources.elevators[self.elevatorNo].request()
        yield elevatorMoving
        floorDelta = np.absolute(self.resources.elevatorPosition[self.elevatorNo]-self.riderStartFloor)
        yield resources.env.timeout(self.resources.travelTimes[floorDelta])
        yield resources.env.timeout(self.timeForDoorsToOpenOrClose)
        travelDelta = np.absolute(self.riderEndFloor - self.riderStartFloor)
        

    def pickServiceingElevator(self):
        servicingElevator = -1
        if self.resources.elevators[0].count < self.resources.elevators[0].capacity:
            servicingElevator = 0
        elif self.resources.elevators[1].count < self.resources.elevators[1].capacity:
            servicingElevator = 1
        elif len(self.resources.elevators[0].queue) < len(self.resources.elevators[1].queue):
            servicingElevator = 0
        else:
            servicingElevator = 1
        return servicingElevator


    def pickRiderFloor(self):
        riderFloor = -1
        
        return riderFloor

    def pickDestinationFloor(self):
        destinationFloor = -1
        
        return destinationFloor
    
    def findElevator(self):
        elevatorPosition = -1
        
        return elevatorPosition

#%%
def riderGenerator(resources):
    riderNo = 1
    while True:
        interarrivalRate = 1
        yield resources.env.timeout(interarrivalRate)
        rider = defaultRider(riderNo, resources)
        resources.env.process(rider.rideElevator())
        riderNo += 1
        noRidersProcessedList.append(1.0)

#%%
noRidersProcessedList = []
resources = simResources()
resources.env.process(riderGenerator(resources))
resources.env.run(until=60.0)
