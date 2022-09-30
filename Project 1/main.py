# -*- coding: utf-8 -*-
"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 1
@description: For this project we are simulating two different drive-thru scenarios. This drive-thru simulation consists of a pair of order stations and payment/pickup window, as space is limited our goal is to optimize throughput of cars to maximize profit during the lunch rush that occurs from 11am - 1pm, or over a 2 hour window.
"""
#%% cell to view graphs

# list of resources
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt


def startDriveThru(env):
    print(f'Simulation time is {env.now:7.3f}')
    yield env.timeout(2.0)
    print(f'Simulation time is {env.now:7.3f}')

env = simpy.Environment()
env.procress(startDriveThru(env))
env.run()

# Watching Lecture on 9/2/22 at timestamp 33:29