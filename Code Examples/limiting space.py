# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:12:28 2022

@author: mrizki
"""

# simulating space between resources

import simpy
import random

def customer(env, custNo, servers, space):
    print(f'customer{custNo} arrives at {env.now:7.3f}')
    req = servers[0].request()
    yield req
    print(f'customer{custNo} starts service with server 0 at {env.now:7.3f}')
    yield env.timeout(1.0)
    print(f'customer{custNo} requests space to move forward at {env.now:7.3f}')   
    spReq = space.request()
    yield spReq
    print(f'customer{custNo} acquires space to move forward at {env.now:7.3f}')     
    servers[0].release(req)
    print(f'customer{custNo} finishes service with server 0 and moves forward at {env.now:7.3f}')    
    req = servers[1].request()
    yield req
    space.release(spReq)
    print(f'customer{custNo} releases space, moves forward, and starts service with server 1 at {env.now:7.3f}')
    yield env.timeout(2.0)
    servers[1].release(req)   
    print(f'customer{custNo} finishes service with server 1 at {env.now:7.3f} and exits')

def customerGenerator(env, servers, space):
    custNo = 0
    while True:
        env.process(customer(env, custNo, servers, space))
        custNo += 1
        yield env.timeout(random.expovariate(1/0.5))


env = simpy.Environment()
servers = [simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1)]
space = simpy.Resource(env, capacity=1)
env.process(customerGenerator(env, servers, space))
env.run(until=10.0)
