# -*- coding: utf-8 -*-
"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 1
@description: For this project we are simulating two different drive-thru scenarios
"""

# list of resources
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

class Customer:
    def __init__(self, number, env, cashier):
        self.custNo = number
        self.env = env
        self.cashier = cashier


def customerGenerator(env, cashier):
    custNo = 0
    while True:
        cust = Customer(custNo, env, cashier)
        env.process(cust.shop())
        custNo += 1
        yield env.timeout(random.expovariate(1/6.0))
