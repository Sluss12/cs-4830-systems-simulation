"""
@author: mSlusser
@class: CS-4830 Systems Simulation
@project: 2
@description: For our second project, we will study how to model and simulate input distributions. Since we have simple queuing simulation experience, we will use the McDonalds restaurant across the street from Wright State as our source of data. 
@file_name: data_processing.
@file_description: data_processing.py is responsible for sample data reading, and processing into usable distributions for our simulation.
"""

#%%
# list of resources
import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
projectDir= os.path.dirname(__file__)
dataDir = os.path.join(projectDir, 'data_sets')
dirList = os.listdir(dataDir)

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

def dataAnalysis(sampleData, descriptor, bins, distribution):

    # Observed
    numBins = bins
    sampleSize = np.size(sampleData)
    sampleMean = np.average(sampleData)
    binEdges = np.linspace(0.0, np.max(sampleData), numBins)
    observed, _ = np.histogram(sampleData,bins=binEdges)
    if distribution == "expo":
        # MLE
        loc, scale = stats.expon.fit(sampleData, floc=0)
        shape=-1
        # Expected
        expectedProb = stats.expon.cdf(binEdges, scale=scale, loc=loc)
        cdf = stats.expon.cdf(sampleData,scale=sampleMean)
    elif distribution == "logNorm":
        # MLE
        shape, loc, scale = stats.lognorm.fit(sampleData, floc=0)
        # Expected
        expectedProb = stats.lognorm.cdf(binEdges, shape, loc=loc ,scale=scale)
        cdf = stats.lognorm.cdf(sampleData, shape, loc=loc, scale=scale)
    expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
    expected = sampleSize * np.diff(expectedProb)
    binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
    chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
    count = np.ones(sampleSize)
    count = np.cumsum(count) / sampleSize
    ks_stat, ks_pValue = stats.ks_2samp(count, cdf)
    
    analysisResults = result(sampleData, descriptor, binEdges, binMidPt, expected, observed,
                              distribution, sampleSize, sampleMean, chiSq, pValue, ks_stat, ks_pValue,
                              shape, loc, scale)
    return analysisResults

def generateInterarrivalTime():
    sampledInterarrivalTimes = getSampledInterarrivalTimes()
    # distribution appears to be: exponential
    results = dataAnalysis(sampledInterarrivalTimes,"Interarrival", 40, "expo")
    return generateValue(results)

def generateOrderTime():
    sampledOrders = getSampledOrders()
    # distribution appears to be: logNormal
    results = dataAnalysis(sampledOrders,"Order", 35, "logNorm")
    return generateValue(results)

def generatePaymentTime():
    sampledPayments = getSampledPayments()
    # distribution appears to be: logNormal
    results = dataAnalysis(sampledPayments,"Payments", 40, "logNorm")
    return generateValue(results)

def generatePickupTime():
    sampledPickups = getSampledPickups()
    # distribution appears to be: logNorm
    results = dataAnalysis(sampledPickups,"Pickups", 45, "logNorm")
    return generateValue(results)

def generateValue(results):
    value = 0
    if results.distribution == "expo":
        value = stats.expon.rvs(loc=results.loc, scale=results.scale, size=1)
        return value[0]
    elif results.distribution == "logNorm":
        value = stats.lognorm.rvs(s=results.shape, loc=results.loc, scale=results.scale, size=1)
        return value[0]
    return TypeError("Incorrect type. Type result required.")

class result:
    def __init__(self, sampleData, descriptor, binEdges, binMidPt, expected, observed,
                 distribution , sampleSize, sampleMean, chiSq, pValue, ks_stat, ks_pValue,
                 shape, loc, scale):
        self.sampleData = sampleData
        self.descriptor = descriptor
        self.binEdges = binEdges
        self.binMidPt = binMidPt
        self.expected = expected
        self.observed = observed
        self.distribution = distribution
        self.sampleSize = sampleSize
        self.sampleMean = sampleMean
        self.chiSq = chiSq
        self.pValue = pValue
        self.ks_stat = ks_stat
        self.ks_pValue = ks_pValue
        self.shape = shape
        self.loc = loc
        self.scale = scale

def output(result):
    print(f'{result.descriptor} Times:')
    print("----------------------------------------")
    print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
    print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')
    print("----")
    print(f'Count: {result.sampleSize}')
    print(f'Mean of {result.descriptor}: {result.sampleMean:.4f}')
    print(f'ChiSquare Statistic: {result.chiSq:0.3f}')
    print(f'P value {result.pValue:0.3f}')
    if result.pValue >= 0.05:
        print('We can not reject the null hypothesis.')
    else:
        print('We reject the null hypothesis.')
    print(f'KS Statistic: {result.ks_stat:0.4f}')
    print(f'KS P Value: {result.ks_pValue:0.4f}')
    if result.ks_pValue >= 0.05:
        print('We can not reject the null hypothesis.')
    else:
        print('We reject the null hypothesis.')
    print("----------------------------------------\n")

def plot(result):
    plt.figure()
    plt.xlabel(f'{result.descriptor} Times')
    plt.ylabel('frequency')
    plt.title(f'Sampled {result.descriptor} Times')
    plt.hist(result.sampleData, bins=result.binEdges, label='Observed')
    plt.plot(result.binMidPt, result.expected, 'or-', label=f'Expected\n({result.distribution})')
    plt.plot(result.binMidPt, result.observed, 'oy-', label='Observed')
    plt.legend()
