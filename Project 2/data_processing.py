"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 2
@description: For our second project, we will study how to model and simulate input distributions. Since we have simple queuing simulation experience, we will use the McDonald’s restaurant across the street from Wright State as our source of data. 
@file_name: data_processing.pyoijfklnh
"""
#%% cell to view graphs

# list of resources
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
DATA_PATH=r"D:\School\Year 5 - Semester 1\CS 4830\cs-4830-systems-simulation\Project 2\data_sets"
dirList = os.listdir(DATA_PATH)

print(dirList)

def importData(files_path=DATA_PATH):
    arrival = import_arrival(files_path)
    order = import_order(files_path)
    payment = import_payment(files_path)
    pickup = import_pickup(files_path)

def import_arrival(files_path):
    fileCounter = 1
    while(True):
        fileNo = str(fileCounter).zfill(2)
        arrivals_path = os.path.join(files_path, "arrival.xlsx")

    return pd.read_csv(arrivals_path)

def import_order(files_path):
    order_path = os.path.join(files_path, "order.csv")
    return pd.read_csv(order_path)

def import_payment(files_path):
    payment_path = os.path.join(files_path, "payment.csv")
    return pd.read_csv(payment_path)

def import_pickup(files_path):
    pickup_path = os.path.join(files_path, "pickup.csv")
    return pd.read_csv(pickup_path)
