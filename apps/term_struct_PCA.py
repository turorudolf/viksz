#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 17:50:48 2019

@author: adamka
"""
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

startYr = 2006 
endYr = 2018
dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, '../data/cache/vixfut' + str(startYr) + '_' + str(endYr) + '.csv')
tab0 = pd.read_csv(fileName)

tab = tab0.loc[tab0.date > '20150101']
dates = list(tab.date.unique())
C = np.outer(np.zeros(7), np.zeros(7))
T = len(dates)
for t in range(1,T):
    # nincs lejaro futures !
    t0 = tab.loc[tab.date==dates[t-1]]
    t1 = tab.loc[tab.date==dates[t]]
    if(t0.loc[t0.num==1].daysToMat.values[0] > 0):
        c0 = t0.close.values
        c1 = t1.open.values
        c0 =c0[0:7]
        c1 =c1[0:7]
        d = c1 - c0
        C += np.outer(d,d)
pca = PCA(n_components=7)
pca.fit(C)
plt.plot(pca.components_[0])
