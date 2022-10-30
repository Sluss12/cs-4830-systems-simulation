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
import numpy as np
import pandas as pd
projectDir= os.path.dirname(__file__)
dataDir = os.path.join(projectDir, 'data_sets')
dirList = os.listdir(dataDir)
print(dataDir)
print(dirList)

def getSampledInterarrivalTimes():
    interarrivalTimes = []
    try:
        for file in dirList:
            fileParts = file.split('.')
            name = fileParts[0]
            ext = fileParts[1]
            fullFileName = dataDir + r"\\" + file
            if name.find('arrival') == 0:
                if ext == 'xlsx':
                    tbl = pd.read_excel(fullFileName)
                    tbl['Time'] = pd.to_datetime(tbl['Time'], format="%I:%M:%S")
                elif ext == 'csv':
                    tbl = pd.read_csv(fullFileName)
                    tbl['Time'] = pd.to_datetime(tbl['Time'])
                tbl['delta'] = (tbl['Time']-tbl['Time'].shift()).fillna(pd.Timedelta(0))
                tbl['elapsedTime'] = tbl['delta'].apply(lambda x: x  / np.timedelta64(1,'s')).astype('int64') % (24*60)
                #print(fullFileName)
                #print(tbl)
                interarrivalTimes += tbl['elapsedTime'].to_list()
    except (KeyError, ValueError, AttributeError) as err:
        print(fullFileName)
        print(err)
    sampledInterarrivalSeconds = interarrivalTimes
    return sampledInterarrivalSeconds

print(getSampledInterarrivalTimes())