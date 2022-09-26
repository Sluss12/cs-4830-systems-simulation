# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:12:28 2022

@author: mrizki
"""

# list of resources

import simpy
import random

def customer(env, custNo, servers):
    
    serverNo = 0
    
    if servers[0].count < servers[0].capacity:
        serverNo = 0
    elif servers[1].count < servers[1].capacity:
       serverNo = 1
    elif len(servers[0].queue) < len(servers[1].queue):
        serverNo = 0
    else:
        serverNo = 1      

    req = servers[serverNo].request()
    yield req
    
    print(f'customer{custNo} starts service with server {serverNo} at {env.now:7.3f}')
    yield env.timeout(2.0)
    
    # spent 2.0 time units being server
    
    servers[serverNo].release(req)
    print(f'customer{custNo} finishes service with server {serverNo} at {env.now:7.3f} and exits')

def customerGenerator(env, servers):
    custNo = 0
    while True:
        env.process(customer(env, custNo, servers))
        custNo += 1
        yield env.timeout(random.expovariate(1/2.0))


env = simpy.Environment()
servers = [simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1)]
env.process(customerGenerator(env, servers))
env.run(until=100.0)
