# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:12:28 2022

@author: mrizki
"""

# mm1 queue
#%%

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
    def __init__(self, number, env, cashier):
        self.custNo = number
        self.env = env
        self.cashier = cashier
        
    def shop(self):
        
        # customer spends time shopping for groceries
        yield env.timeout(random.expovariate(1/15.0))
        
        # customer get in line to check out
        joinLineTime = self.env.now
        
        req = self.cashier.request()
        yield req
        
        waitTime = self.env.now - joinLineTime
        waitTimeList.append(waitTime)
        
        #print(f'wait time {self.waitTime}')
        
        # customer obtains the cashier and take a random time to check out
        yield env.timeout(random.expovariate(1/5.0))
        
        # customer leave the check out
        self.cashier.release(req)
        
def customerGenerator(env, cashier):
    custNo = 0
    while True:
        cust = Customer(custNo, env, cashier)
        env.process(cust.shop())
        custNo += 1
        yield env.timeout(random.expovariate(1/6.0))

averageWaitTime = []
for replicate in range(100):
    waitTimeList = []
    env = simpy.Environment()
    cashier = simpy.Resource(env, capacity=1)
    env.process(customerGenerator(env, cashier))
    env.run(until=200.0)
    #print(waitTimeList)
    #print(f'average wait time is {np.average(waitTimeList)}')
    averageWaitTime.append(np.average(waitTimeList))

print(averageWaitTime)
print(f'The average wait time is {np.average(averageWaitTime):0.3}')

plt.figure()
plt.plot(averageWaitTime)
plt.bar(range(len(averageWaitTime)), averageWaitTime)
plt.show()

plt.figure()
plt.hist(averageWaitTime, bins=20)
plt.xlabel('average wait time')
plt.ylabel('frequency')
plt.title('expereimental results')
plt.show()