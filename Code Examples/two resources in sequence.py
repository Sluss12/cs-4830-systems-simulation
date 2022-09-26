# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:12:28 2022

@author: mrizki
"""

# list of resources

import simpy
import random

def customer(env, custNo, servers):
    # requesting first server (resource)
    
    print(f'customer{custNo} arrives at {env.now:7.3f}')
    req = servers[0].request()
    yield req
    
    # we got the first server
    
    print(f'customer{custNo} starts service with server 0 at {env.now:7.3f}')
    yield env.timeout(2.0)
    
    # spent 2.0 time units being server
    
    # release the first server
    servers[0].release(req)
    
    # request second server
    req = servers[1].request()
    print(f'customer{custNo} finishes service with server 0 at {env.now:7.3f}')
    yield req
    
    # we got the second server
    
    print(f'customer{custNo} starts service with server 1 at {env.now:7.3f}')
    yield env.timeout(2.0)
    
    # spent 2.0 time units being served at the second server
    
    servers[1].release(req)  
    
    # release second server
    
    print(f'customer{custNo} finishes service with server 1 at {env.now:7.3f} and exits')

def customerGenerator(env, servers):
    custNo = 0
    while True:
        env.process(customer(env, custNo, servers))
        custNo += 1
        yield env.timeout(random.expovariate(1/2.0))


env = simpy.Environment()
servers = [simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1)]
env.process(customerGenerator(env, servers))
env.run(until=10.0)
