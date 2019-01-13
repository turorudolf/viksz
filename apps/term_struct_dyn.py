#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 17:50:48 2019

@author: adamka
"""
import os
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#from sklearn.decomposition import PCA

startYr = 2006 
endYr = 2018
dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, '../data/cache/vixfut' + str(startYr) + '_' + str(endYr) + '.csv')
DF0 = pd.read_csv(fileName)
DF0['date'] = pd.to_datetime(DF0.date)
df = DF0.loc[DF0.date > datetime.date(2012, 1, 1)]
dates = list(df.date.unique())
x = y = dF = conts = np.array([])
date_length = len(dates)

# todo: manage nans !!
# what if we have backwardation ??
for d in range(3,date_length):
    # nincs lejaro futures !
    df0 = df.loc[df.date==dates[d-1]]
    df1 = df.loc[df.date==dates[d]]
    if(df0.loc[df0.num==1].daysToMat.values[0] > 0):
        t0 = df0.daysToMat.values
        c0 = df0.close.values
        c1 = df1.close.values
        cont = (c0[1]-c0[0])
        if(cont > 0):
            x = np.append(x, c0[1]-c0[0] ) 
            y = np.append(y, c0[1]-c1[0] )
            conts = np.append(conts, c0[1]-c0[0])
            dF = np.append(dF, c0[0]-c1[0])
#plt.plot(x, y,'o')
plt.plot(np.cumsum(y))
#plt.hist(conts-dF,bins=75)
