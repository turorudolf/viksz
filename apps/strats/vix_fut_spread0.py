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

x = y = dF = conts = profit = np.array([])
dates_ = []
date_length = len(dates)
sign = -1
pos = [0, 0]
init_price = [0, 0]
pnl = [0]
cont = 0

for d in range(0,date_length):
    # nincs lejaro futures !
    df0 = df.loc[df.date==dates[d]]
    t0 = df0.daysToMat.values
    settle = df0.settle.values
    c0 = df0.close.values
    # eleg jo a profit v nagy a buko --> exit
    profit_now_1 = pos[0]*(c0[0] - init_price[0])
    profit_now_2 = pos[1]*(c0[1] - init_price[1])
    profit_tot = profit_now_1+profit_now_2
    #if(profit_tot != 0):
    #    print(profit_now_1+profit_now_2)
    if(profit_tot > 10):
        print("exit on gain, pos=",pos,"date:",dates[d],"pnl=",profit_tot)
        pnl = np.append(pnl,profit_tot)
        pos = [0,0]
        init_price = [0,0]
    elif(c0[1] - c0[0] < -1.5 and pos!=[0,0]):
        print("exit on backward, pnl=",profit_tot)
        pnl = np.append(pnl,profit_tot)
        pos = [0,0]
        init_price = [0,0]
    # elso lejar
    elif(t0[0] == 0 and pos[0] != 0):
        #print("1.lejart")
        pnl = np.append(pnl, pos[0]*(settle[0] - init_price[0]))
        print("exit 1., pnl=", pnl[-1])
        #pnl = np.append(pnl, -(pos[0]*price[0]+pos[1]*price[1])/2 )
        pos[0] = 0
    # masodik lejar
    elif(t0[0] == 0 ):
        if(pos[1]!= 0 and pos[0] == 0):
            pnl = np.append(pnl, pos[1]*(settle[0] - init_price[1]))
            print("exit 2., pnl=", pnl[-1])
            pos[1] = 0
            #pnl = np.append(pnl, -(pos[0]*price[0]+pos[1]*price[1])/2 )
        cont = c0[2] - c0[1]
        conts = np.append(conts, cont)
        if(cont/(c0[1]+c0[2])*2  >= 0.02):
            pos = [np.sign(cont), -np.sign(cont)]
            print("enter, date:",dates[d])
        else:
             pos = [0,0]
              #print("...contango is śmall")
        init_price = [c0[1], c0[2]]
        dates_.append(dates[d])
#plt.plot(conts)
#plt.plot(np.cumsum(profit+noise))
plt.plot(np.cumsum(pnl))
