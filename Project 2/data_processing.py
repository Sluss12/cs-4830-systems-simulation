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

interarrivalTimes = []

for file in dirList:
    fileParts = file.split('.')
    
    nameWithNo = fileParts[0]
    ext = fileParts[1]
    nameParts = nameWithNo.split('_')
    name = nameParts[0]
    fileNo = nameParts[1]
    
    fullFileName = DATA_PATH + r"\\" + file
    
    if name.find('arrival') == 0:
        if ext == 'xlsx':
            tbl = pd.read_excel(fullFileName)
            tbl['Arrivals'] = pd.to_datetime(tbl['Arrivals'], format="%I:%M:%S")
        elif ext == 'csv':
            tbl = pd.read_csv(fullFileName)
            tbl['Arrivals'] = pd.to_datetime(tbl['Arrivals'])

        tbl['delta'] = (tbl['Arrivals']-tbl['Arrivals'].shift()).fillna(pd.Timedelta(0))     
        tbl['elapsedTime'] = tbl['delta'].apply(lambda x: x  / np.timedelta64(1,'s')).astype('int64') % (24*60)
        print(tbl)

        interarrivalTimes += tbl['elapsedTime'].to_list()
        
sampleData = interarrivalTimes
