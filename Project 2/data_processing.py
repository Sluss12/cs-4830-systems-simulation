"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 2
@description: For our second project, we will study how to model and simulate input distributions. Since we have simple queuing simulation experience, we will use the McDonalds restaurant across the street from Wright State as our source of data. 
@file_name: data_processing.
@file_description: data_processing.py is responsible for sample data reading, and processing into usable distributions for our simulation.
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
#print(dirList)

def getSampledInterarrivalTimes():
    interarrivalTimes = []
    for file in dirList:
        try:
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
                interarrivalTimes += tbl['elapsedTime'].to_list()
                # print(fullFileName)
                # print(tbl)
        except (KeyError, ValueError, AttributeError) as err:
            print(fullFileName)
            print(err)
    sampledInterarrivalSeconds = interarrivalTimes
    return sampledInterarrivalSeconds

def getSampledOrders():
    orderTimes = []
    for file in dirList:
        try:
            fileParts = file.split('.')
            name = fileParts[0]
            ext = fileParts[1]
            fullFileName = dataDir + r"\\" + file
            if name.find('order') == 0:
                if ext == 'xlsx':
                    tbl = pd.read_excel(fullFileName)
                    tbl['Start'] = pd.to_datetime(tbl['Start'], format="%I:%M:%S")
                    tbl['Stop'] = pd.to_datetime(tbl['Stop'], format="%I:%M:%S")
                elif ext == 'csv':
                    tbl = pd.read_csv(fullFileName)
                    tbl['Start'] = pd.to_datetime(tbl['Start'])
                    tbl['Stop'] = pd.to_datetime(tbl['Stop'])
                tbl['delta'] = (tbl['Stop']-tbl['Start']).fillna(pd.Timedelta(0))
                tbl['elapsedTime'] = tbl['delta'].apply(lambda x: x  / np.timedelta64(1,'s')).astype('int64') % (24*60)
                orderTimes += tbl['elapsedTime'].to_list()
                # print(fullFileName)
                # print(tbl)
        except (KeyError, ValueError, AttributeError) as err:
            print(fullFileName)
            print(err)
    sampledOrderSeconds = orderTimes
    return sampledOrderSeconds

def getSampledPayments():
    paymentTimes = []
    for file in dirList:
        try:
            fileParts = file.split('.')
            name = fileParts[0]
            ext = fileParts[1]
            fullFileName = dataDir + r"\\" + file
            if name.find('payment') == 0:
                if ext == 'xlsx':
                    tbl = pd.read_excel(fullFileName)
                    tbl['Start'] = pd.to_datetime(tbl['Start'], format="%I:%M:%S")
                    tbl['Stop'] = pd.to_datetime(tbl['Stop'], format="%I:%M:%S")
                elif ext == 'csv':
                    tbl = pd.read_csv(fullFileName)
                    tbl['Start'] = pd.to_datetime(tbl['Start'])
                    tbl['Stop'] = pd.to_datetime(tbl['Stop'])
                tbl['delta'] = (tbl['Stop']-tbl['Start']).fillna(pd.Timedelta(0))
                tbl['elapsedTime'] = tbl['delta'].apply(lambda x: x  / np.timedelta64(1,'s')).astype('int64') % (24*60)
                paymentTimes += tbl['elapsedTime'].to_list()
                # print(fullFileName)
                # print(tbl)
        except (KeyError, ValueError, AttributeError) as err:
            print(fullFileName)
            print(err)
    sampledPaymentSeconds = paymentTimes
    return sampledPaymentSeconds

def getSampledPickups():
    pickupTimes = []
    for file in dirList:
        try:
            fileParts = file.split('.')
            name = fileParts[0]
            ext = fileParts[1]
            fullFileName = dataDir + r"\\" + file
            if name.find('pickup') == 0:
                if ext == 'xlsx':
                    tbl = pd.read_excel(fullFileName)
                    tbl['Start'] = pd.to_datetime(tbl['Start'], format="%I:%M:%S")
                    tbl['Stop'] = pd.to_datetime(tbl['Stop'], format="%I:%M:%S")
                elif ext == 'csv':
                    tbl = pd.read_csv(fullFileName)
                    tbl['Start'] = pd.to_datetime(tbl['Start'])
                    tbl['Stop'] = pd.to_datetime(tbl['Stop'])
                tbl['delta'] = (tbl['Stop']-tbl['Start']).fillna(pd.Timedelta(0))
                tbl['elapsedTime'] = tbl['delta'].apply(lambda x: x  / np.timedelta64(1,'s')).astype('int64') % (24*60)
                pickupTimes += tbl['elapsedTime'].to_list()
                # print(fullFileName)
                # print(tbl)
        except (KeyError, ValueError, AttributeError) as err:
            print(fullFileName)
            print(err)
    sampledPickupSeconds = pickupTimes
    return sampledPickupSeconds

print("Interarrival Times:")
sampledInterarrivalTimes = getSampledInterarrivalTimes()
print(sampledInterarrivalTimes)
print("----------------------------------------")
print(f'Mean of Interarrivals: {np.average(sampledInterarrivalTimes):.4f}')
print("========================================")
print("Order Times:")
sampledOrders = getSampledOrders()
print(sampledOrders)
print("----------------------------------------")
print(f'Mean of Orders: {np.average(sampledOrders):.4f}')
print("========================================")
print("Payment Times:")
sampledPayments = getSampledPayments()
print(sampledPayments)
print("----------------------------------------")
print(f'Mean of Payments: {np.average(sampledPayments):.4f}')
print("========================================")
print("Pickup Times:")
sampledPickups = getSampledPickups()
print(sampledPickups)
print("----------------------------------------")
print(f'Mean of Pickups: {np.average(sampledPickups):.4f}')

#%%