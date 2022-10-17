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
from scipy.stats import lognorm
import random

# Customer Simulation Process
class Customer:
  def __init__(self, env, pumps, custNo):
    self.env = env
    self.pumps = pumps
    self.custNo = custNo
    self.sideNum = -1
    self.pumpNum = -1
    scale = 1.5
    shape = 0.5
    self.payAndPumpTime = lognorm.rvs(scale, 0,shape, size=1)

  def pumpGas(self):
    if ((len(self.pumps[0][0].queue) + self.pumps[0][0].count) < (len(self.pumps[1][0].queue) + self.pumps[1][0].count)):
      self.sideNum = 0
      self.pumpNum = 0
    else:
      self.sideNum = 1
      self.pumpNum = 0
    getToPump = self.pumps[self.sideNum][self.pumpNum].request()
    yield getToPump
    if (self.pumps[self.sideNum][1].count < self.pumps[self.sideNum][1].capacity):
      self.pumpNum+=1
      goToSecondPump = self.pumps[self.sideNum][self.pumpNum].request()
      yield goToSecondPump
      yield self.pumps[self.sideNum][self.pumpNum-1].release(getToPump)
    yield self.env.timeout(self.payAndPumpTime)
    if (self.pumpNum == 0):
      yield self.pumps[self.sideNum][self.pumpNum].release(getToPump)
    else:
      yield self.pumps[self.sideNum][self.pumpNum].release(goToSecondPump)


# Customer Generator Process
def customerGenerator(env, pumps):
  meanInterarrivalTime = 5.0
  customerNo = 1
  while True:
    interarrivalRate = random.expovariate(1/meanInterarrivalTime)
    yield env.timeout(interarrivalRate)
    customer = Customer(env, pumps, customerNo)
    env.process(customer.pumpGas())
    customerNo += 1

# Process and Resource Creations
env = simpy.Environment()
pumpsOneAndTwo = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
pumpsThreeAndFour = [simpy.Resource(env,capacity=1), simpy.Resource(env, capacity=1)]
pumps = [pumpsOneAndTwo, pumpsThreeAndFour]
env.process(customerGenerator(env, pumps))
env.run(until=17*60)
