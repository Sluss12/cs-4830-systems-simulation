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
  def __init_(self, env, pumps):
    self.env = env
    self.pumps = pumps
    self.onPump = -1
    

# Customer Generator Process
meanInterarrivalTime = 5.0
def customerGenerator(env, pumps):
  while True:
    interarrivalRate = random.expovariate(1/meanInterarrivalTime)  # delay between customers
    yield env.timeout(interarrivalRate)
    customer = Customer(env, pumps)

# Process and Resource Creations
env = simpy.Environment()
pumpsOneAndTwo = [simpy.Resource(env, capacity=1), simpy.Resource(env, capacity=1)]
pumpsThreeAndFour = [simpy.Resource(env,capacity=1), simpy.Resource(env, capacity=1)]
pumps = [pumpsOneAndTwo, pumpsThreeAndFour]
env.process(customerGenerator(env, pumps))
env.run(until=17.0*60.0)  # until=hours*60-minutes, hours=17
