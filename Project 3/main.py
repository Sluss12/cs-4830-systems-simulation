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
import simpy
import random
import numpy as np

#%%
class elevator(simpy.Resource):
    def __init__(self, env: simpy.Environment, capacity: int = 1, 
                 position: int = 1 , destination: int = 0 ):
        super().__init__(env, capacity)
        self.position = position
        self.destination = destination
    
    def travelDelta(self) -> int:
        return np.abs(self.destination-self.position)
    
    def travelTime(self):
        travelTime =random.uniform(9.5, 11.0) * self.travelDelta()
        print(f'Travel time = {travelTime}')
        return travelTime

class simResources:
    def __init__(self):
        self.env = simpy.Environment()
        self.elevator = [elevator(self.env, capacity=1, ),
                          elevator(self.env, capacity=1)]

#%%
class rider:
    def __init__(self, riderNo: int, resources: simResources):
        self.riderNo = riderNo
        self.env = resources.env
        self.elevator = resources.elevator
        self.elevatorNo = -1
        self.elevatorStartFloor = -1
        self.startFloor = -1
        self.endFloor = -1
        self.timeForElevatorToArrive = -1
        self.timeForDoorsToOpenOrClose = 3
        self.timeForElevatorToTravel = -1
        # For Use in Stats
        self.timeOfRiderArrival = -1
        self.timeOfElevatorArrival = -1
        self.waitTime = -1
        # end __init__
    
    def rideElevator(self):
        pass
    def floorDelta(self) -> int:
        return np.abs(self.elevator[self.elevatorNo].position - self.startFloor)
    def travelDelta(self) -> int:
        return self.elevator[self.elevatorNo].travelDelta()
    def travelTime(self):
        return self.elevator[self.elevatorNo].travelTime()
    def findElevator(self)-> int:
        return self.elevator[self.elevatorNo].position
    def getWaitTime(self):
        self.waitTime = self.timeOfElevatorArrival + self.timeForDoorsToOpenOrClose - self.timeOfRiderArrival
        return self.waitTime
    def pickServiceingElevator(self) -> int:
        if self.elevator[0].count == 0 and self.elevator[1].count == 0: #none in use, pick the closest
            if np.abs(self.elevator[0].position - self.startFloor) < np.abs(self.elevator[1].position - self.startFloor):
                return 0
            else:
                return 1
        else:
            if self.elevator[0].count < self.elevator[0].capacity:
                return 0
            elif self.elevator[1].count < self.elevator[1].capacity:
                return 1
            elif len(self.elevator[0].queue) < len(self.elevator[1].queue):
                return 0
            else:
                return 1
    # end def
    def pickStartFloor(self):
        floor = -1
        floors=[0,1,2,3,4]
        # I am estimating that 5% of people start in the basement, 40% start on the first floor, 
        # 20% start on the second floor, 27% start on the third floor, and 8% start on the fourth floor
        floor = random.choices(floors,cum_weights=[5,45,65,92,100])
        print(f'Start Floor Picked: {floor[0]}')
        self.startFloor = floor[0]
    # end def
    def pickDestinationFloor(self):
        floor = -1
        floors=[0,1,2,3,4]
        # I am estimating that 5% of people end in the basement, 45% end on the first floor, 
        # 15% end on the second floor, 25% end on the third floor, and 10% end on the fourth floor
        while floor == -1 or floor[0] == self.startFloor:
            floor = random.choices(floors,cum_weights=[5,50,65,90,100])
        print(f'End Floor Picked: {floor[0]}')
        self.endFloor = floor[0]
    # end def
    
    def riderArrivalMessage(self) -> str:
        return f'Rider {self.riderNo} has arrived at {self.env.now:.2f} on floor {self.startFloor}, the elevators are on floors {self.elevator[0].position}, and {self.elevator[1].position}'
    def riderOnMessage(self) -> str:
        return f'Rider {self.riderNo} got on elevator {self.elevatorNo}'
    def riderDestinationMessage(self) -> str:
        return f'Rider {self.riderNo} is on the elevator and going to floor {self.elevator[self.elevatorNo].destination}'
    def riderExitMessage(self) -> str:
        return f'Rider {self.riderNo} got off elevator {self.elevatorNo} at {self.env.now:.3f}'
    def elevatorRequestMessage(self) -> str:
        return f'Rider {self.riderNo} has requested elevator {self.elevatorNo}'
    def elevatorMovingMessage(self) -> str:
        return f'Elevator {self.elevatorNo} is on it way to floor {self.startFloor} from floor {self.elevatorStartFloor}'
    def elevatorArrivalMessage(self) -> str:
        return f'Elevator {self.elevatorNo} arrived at floor {self.elevator[self.elevatorNo].position} at {self.env.now:.3f}'
    def elevatorDestinationMessage(self) -> str:
        return f'Elevator {self.elevatorNo} brought rider {self.riderNo} to floor {self.elevator[self.elevatorNo].position} at {self.env.now:.3f}'
    def elevatorReleasedMessage(self) -> str:
        return f'Elevator {self.elevatorNo} was released by rider {self.riderNo} at {self.env.now:.3f}'
    def returnedToFloorMessage(self) -> str:
        return f'Elevator {self.elevatorNo} returned to floor {self.elevator[self.elevatorNo].position}'

class defaultElevator(rider):
    def rideElevator(self):
        self.timeOfRiderArrival = self.env.now
        self.pickStartFloor()
        self.pickDestinationFloor()
        print(self.riderArrivalMessage())
        self.elevatorNo = self.pickServiceingElevator()
        callElevator = self.elevator[self.elevatorNo].request()
        self.elevatorStartFloor = self.findElevator()
        print(self.elevatorRequestMessage())
        yield callElevator # elevator is ready to move to called floor
        self.elevator[self.elevatorNo].destination = self.startFloor # update elevator destination once the rider has the elevator
        print(self.elevatorMovingMessage())
        self.timeForElevatorToArrive = self.travelTime()
        yield self.env.timeout(self.timeForElevatorToArrive) # elevator arrives to correct starting floor
        self.timeOfElevatorArrival = self.env.now
        self.elevator[self.elevatorNo].position = self.startFloor # update elevator position to startFloor
        print(self.elevatorArrivalMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        print(self.riderOnMessage())
        self.elevator[self.elevatorNo].destination = self.endFloor # rider is on the elevator, update destination
        self.timeForElevatorToTravel = self.travelTime()
        print(self.riderDestinationMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose) # doors close, elevator is ready to leave
        self.elevator[self.elevatorNo].position = self.endFloor # update elevator position to endFloor AS the elevator leaves
        yield self.env.timeout(self.timeForElevatorToTravel)
        print(self.elevatorDestinationMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        print(self.riderExitMessage())
        yield self.elevator[self.elevatorNo].release(callElevator)
        print(self.elevatorReleasedMessage())
        waitTimeList.append(self.getWaitTime())

class idleOneElevator(rider):
    def rideElevator(self):
        self.timeOfRiderArrival = self.env.now
        self.pickStartFloor()
        self.pickDestinationFloor()
        print(self.riderArrivalMessage())
        self.elevatorNo = self.pickServiceingElevator()
        callElevator = self.elevator[self.elevatorNo].request()
        self.elevatorStartFloor = self.findElevator()
        print(self.elevatorRequestMessage())
        yield callElevator # elevator is ready to move to called floor
        self.elevator[self.elevatorNo].destination = self.startFloor # update elevator destination once the rider has the elevator
        print(self.elevatorMovingMessage())
        self.timeForElevatorToArrive = self.travelTime()
        yield self.env.timeout(self.timeForElevatorToArrive) # elevator arrives to correct starting floor
        self.timeOfElevatorArrival = self.env.now
        self.elevator[self.elevatorNo].position = self.startFloor # update elevator position to startFloor
        print(self.elevatorArrivalMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        print(self.riderOnMessage())
        self.elevator[self.elevatorNo].destination = self.endFloor # rider is on the elevator, update destination
        self.timeForElevatorToTravel = self.travelTime()
        print(self.riderDestinationMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose) # doors close, elevator is ready to leave
        self.elevator[self.elevatorNo].position = self.endFloor # update elevator position to endFloor AS the elevator leaves
        yield self.env.timeout(self.timeForElevatorToTravel)
        print(self.elevatorDestinationMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        print(self.riderExitMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        if len(self.elevator[self.elevatorNo].queue) == 0: # no one is waiting on this elevator, send to first floort
            self.elevator[self.elevatorNo].destination = 1
            yield self.env.timeout(self.elevator[self.elevatorNo].travelTime())
            self.elevator[self.elevatorNo].position = 1
            print(self.returnedToFloorMessage())
        yield self.elevator[self.elevatorNo].release(callElevator)
        print(self.elevatorReleasedMessage())
        waitTimeList.append(self.getWaitTime())

class sequenceElevator(defaultElevator):
    def pickServiceingElevator(self) -> int:
        if self.endFloor > self.startFloor:
            return 0
        else:
            return 1

class oneFourElevator(rider):
    def rideElevator(self):
        self.timeOfRiderArrival = self.env.now
        self.pickStartFloor()
        self.pickDestinationFloor()
        print(self.riderArrivalMessage())
        self.elevatorNo = self.pickServiceingElevator()
        callElevator = self.elevator[self.elevatorNo].request()
        self.elevatorStartFloor = self.findElevator()
        print(self.elevatorRequestMessage())
        yield callElevator # elevator is ready to move to called floor
        self.elevator[self.elevatorNo].destination = self.startFloor # update elevator destination once the rider has the elevator
        print(self.elevatorMovingMessage())
        self.timeForElevatorToArrive = self.travelTime()
        yield self.env.timeout(self.timeForElevatorToArrive) # elevator arrives to correct starting floor
        self.timeOfElevatorArrival = self.env.now
        self.elevator[self.elevatorNo].position = self.startFloor # update elevator position to startFloor
        print(self.elevatorArrivalMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        print(self.riderOnMessage())
        self.elevator[self.elevatorNo].destination = self.endFloor # rider is on the elevator, update destination
        self.timeForElevatorToTravel = self.travelTime()
        print(self.riderDestinationMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose) # doors close, elevator is ready to leave
        self.elevator[self.elevatorNo].position = self.endFloor # update elevator position to endFloor AS the elevator leaves
        yield self.env.timeout(self.timeForElevatorToTravel)
        print(self.elevatorDestinationMessage())
        yield self.env.timeout(self.timeForDoorsToOpenOrClose)
        print(self.riderExitMessage())
        if len(self.elevator[self.elevatorNo].queue) == 0: # no one is waiting on this elevator. if 0 send to first floor, if 1 send to second floor
            if self.elevatorNo == 0:
                self.elevator[self.elevatorNo].destination = 1
                yield self.env.timeout(self.elevator[self.elevatorNo].travelTime())
                self.elevator[self.elevatorNo].position = 1
            else:
                self.elevator[self.elevatorNo].destination = 4
                yield self.env.timeout(self.elevator[self.elevatorNo].travelTime())
                self.elevator[self.elevatorNo].position = 4
            print(self.returnedToFloorMessage())
        yield self.elevator[self.elevatorNo].release(callElevator)
        print(self.elevatorReleasedMessage())
        waitTimeList.append(self.getWaitTime())

#%%
def defaultGenerator(resources):
    riderNo = 1
    while True:
        
        interarrivalRate = random.expovariate(1/meanInterArrivalTime)
        yield resources.env.timeout(interarrivalRate)
        rider = defaultElevator(riderNo, resources)
        resources.env.process(rider.rideElevator())
        riderNo += 1
        noRidersProcessedList.append(1.0)
    # end def

def idleOneGenerator(resources):
    riderNo = 1
    while True:
        interarrivalTime = random.expovariate(1/meanInterArrivalTime)
        yield resources.env.timeout(interarrivalTime)
        rider = idleOneElevator(riderNo, resources)
        resources.env.process(rider.rideElevator())
        riderNo += 1
        noRidersProcessedList.append(1.0)
    # end def

def sequenceGenerator(resources):
    riderNo = 1
    while True:
        interarrivalRate = random.expovariate(1/meanInterArrivalTime)
        yield resources.env.timeout(interarrivalRate)
        rider = sequenceElevator(riderNo, resources)
        resources.env.process(rider.rideElevator())
        riderNo += 1
        noRidersProcessedList.append(1.0)
    # end def

def oneFourGenerator(resources):
    riderNo = 1
    while True:
        interarrivalRate = random.expovariate(1/meanInterArrivalTime)
        yield resources.env.timeout(interarrivalRate)
        rider = oneFourElevator(riderNo, resources)
        resources.env.process(rider.rideElevator())
        riderNo += 1
        noRidersProcessedList.append(1.0)
    # end def
#%%
meanInterArrivalTime = 25 #seconds

noRidersProcessedList = []
waitTimeList = []
resources = simResources()
resources.env.process(defaultGenerator(resources))
# resources.env.process(idleOneGenerator(resources))
# resources.env.process(sequenceGenerator(resources))
# resources.env.process(oneFourGenerator(resources))
resources.env.run(until=300.0)
print(f'Riders Proccessed: {np.sum(noRidersProcessedList):0.0f}')
print(f'Average Wait Time: {np.average(waitTimeList)}')
print(f'Wait Times: {waitTimeList}')
print('\n\n\n\n\n')
