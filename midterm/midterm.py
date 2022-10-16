"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: midterm
@description: We want to simulate the behavior of a small gas station that has one island containing two gasoline pumps. 
Customer arrivals are modeled using an exponentially distributed random variable with a mean interarrival time of 5 minutes.
Assume the transaction time (pay and pump gas) for customers is modeled using lognormal distribution with a scale value of 1.5 and a shape parameter of 0.5. 
A lognormal with a scale and shape of these values produces a mean of approximately 5 minutes. 
Once the transaction is complete the customer exits the gas station. 
"""
# Imports
import simpy
import random

# Customer Simulation Process
class Customer:
  def __init__(self, env, pumps):
    self.env = env
    self.pumps = pumps
    self.sideNum = -1
    self.pumpNum = -1
    self.payAndPumpTime = random.lognormvariate(1.5, 0.5)
    
  def pumpGas(self):
    # check which side has fewer people waiting
    if (len(self.pumps[0][0].queue) < len(self.pumps[1][0].queue)):
      self.sideNum = 0
      self.pumpNum = 0
    else:
      self.sideNum = 1
      self.pumpNum = 0
      print(f'Customer went to side {self.sideNum}')
      
    # get in line for the first pump on the chosen side
    getToPump = self.pumps[self.sideNum][self.pumpNum].request()
    yield getToPump  # first pump free
    print(f'Customer got to the first pump on side {self.sideNum}')
    # once the first pump is free check if the second pump is as well
    if (self.pumps[self.sideNum][1].count < self.pumps[self.sideNum][1].capacity):  
      # if the second pump is free move forward and release first pump
      print(f'The second pump is open on side {self.sideNum}, customer is pullig forward')
      self.pumpNum+=1
      goToSecondPump = self.pumps[self.sideNum][self.pumpNum].request()
      yield goToSecondPump
      yield self.pumps[self.sideNum][self.pumpNum-1].release(getToPump)
    # At the pump
    print(f'Customer is now pumping gas on side {self.sideNum} pump {self.pumpNum}')
    yield self.env.timeout(self.payAndPumpTime)
    # Finished pumping gas, ready to leave and release the pump
    if (self.pumpNum == 0):
      yield self.pump[self.sideNum][self.pumpNum].release(getToPump)
    else:
      yield self.pump[self.sideNum][self.pumpNum].release(goToSecondPump)
    print(f'Customer has left. Now side {self.sideNum} pump {self.pumpNum} is free.')


# Customer Generator Process
meanInterarrivalTime = 5.0
def customerGenerator(env, pumps):
  while True:
    interarrivalRate = random.expovariate(1/meanInterarrivalTime)  # delay between customers
    yield env.timeout(interarrivalRate)
    customer = Customer(env, pumps)
    env.process(customer.pumpGas())

# Process and Resource Creations
env = simpy.Environment()
pumpsOneAndTwo = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
pumpsThreeAndFour = [simpy.Resource(env,capacity=1), simpy.Resource(env, capacity=1)]
pumps = [pumpsOneAndTwo, pumpsThreeAndFour]
#pumps = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
env.process(customerGenerator(env, pumps))
env.run(until=1.0*60.0)  # until=hours*60-minutes, hours=17
