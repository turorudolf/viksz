#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 19:57:38 2019

@author: adamka
"""

import os
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, '../data/IB/1day/' + 'VIX_20080825_20180820.csv')
DF = pd.read_csv(fileName)
d = 5
n_points = 200
n = d * n_points
c = DF.close[0:n]
r = np.arange(0, n, d)
c_d = DF.close[r]
#plt.plot(c_d.diff(1).shift(1),c_d.diff(1),'o')
s = np.array([1,-1]*int(n_points/2))
plt.plot(np.cumsum(c_d*s))