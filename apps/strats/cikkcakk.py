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
fileName = os.path.join(dirname, '../../data/cache/vixfut' + str(startYr) + '_' + str(endYr) + '.csv')
DF0 = pd.read_csv(fileName)
DF0['date'] = pd.to_datetime(DF0.date)
df = DF0.loc[DF0.date > datetime.date(2007, 1, 1)]
dates = list(df.date.unique())

x = y = dF = conts = noise = profit =  np.array([])
dates_ = []
date_length = len(dates)
sign = -1
pos = [0, 0]
init_price = [0, 0]
pnl = 0
cont = 0

# todo: manage nans, take positions !!
# what if we have backwardation ??
"""
for d in range(0,date_length):
    # nincs lejaro futures !
    df0 = df.loc[df.date==dates[d]]
    t0 = df0.daysToMat.values
    settle = df0.settle.values
    c0 = df0.close.values
    if(t0[0] == 0 and pos[0] != 0):
        noise = np.append(noise, -pos[0]*settle[0])
        profit = np.append(profit, np.abs(cont)/2)
        pos[0] = 0
    elif(t0[0] == 0):
        noise = np.append(noise, -pos[1]*settle[0])
        profit = np.append(profit, np.abs(cont)/2)
        cont = c0[2]-c0[1]
        conts = np.append(conts, cont)
        pos = [np.sign(cont), -np.sign(cont)]
        dates_.append(dates[d])
"""
for d in range(0,date_length):
    # nincs lejaro futures !
    df0 = df.loc[df.date==dates[d]]
    t0 = df0.daysToMat.values
    settle = df0.settle.values
    c0 = df0.close.values
    # eleg jo a profit -> exit
    profit_now = pos[0]*(c0[0] - init_price[0]) + pos[1]*(c0[1] - init_price[1])
    if(profit_now > 1):
        print("exit on gain, pos=",pos,"pnl=",profit_now)
        pnl = np.append(pnl,profit_now)
        pos = [0,0]
        init_price = [0,0]
    # elso lejar
    elif(t0[0] == 0 and pos[0] != 0):
        #print("1.lejart")
        pnl = np.append(pnl, pos[0]*(settle[0] - init_price[0]))
        print("exit 1., pnl=", pos[0]*(settle[0] - init_price[0]))
        #pnl = np.append(pnl, -(pos[0]*price[0]+pos[1]*price[1])/2 )
        pos[0] = 0
    # masodik lejar
    elif(t0[0] == 0 ):
        if(pos[1]!= 0):
            pnl = np.append(pnl, pos[1]*(settle[0] - init_price[1]))
            print("exit 2., pnl=", pos[1]*(settle[0] - init_price[1]))
            #pnl = np.append(pnl, -(pos[0]*price[0]+pos[1]*price[1])/2 )
        cont = c0[2] - c0[1]
        if(np.abs(cont) < 0.2):
            print("...contango is śmall")
            pos = [0,0]
        conts = np.append(conts, cont)
        pos = [-np.sign(cont), np.sign(cont)]
        if(pos[0]!= 0):
            print("enter")
        init_price = [c0[1], c0[2]]
        dates_.append(dates[d])
#plt.plot(conts)
#plt.plot(np.cumsum(profit+noise))
plt.plot(np.cumsum(pnl))
