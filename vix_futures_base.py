import modules.futuresData as ft
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# load data
futTab = ft.readFuturesData(range(2018,2019))
futTab = futTab.sort_values(['date','expiry'])
dates = futTab.date.unique()
futTab.loc[:,'slope'] = np.nan

#
# BAROMI LASSU IGY!
#
print "Setting ordinal numbers and slopes..."
for date in dates:
    f = futTab[futTab.date==date]
    futTab.loc[futTab.date==date,'num'] = range(1, len(f) + 1)
    futTab.loc[futTab.date==date,'slope'] = f.settle - f.settle.shift(1)

# todo1: set multiplier before ~2008 it was *10 -- OK
# todo:1.1 fix indexing
# todo:1.2 fix 0 prices
# todo2: set ordinal number of contract for each date! -- OK
# todo3: join w/ VIX tab and set slopes for front contracts!
# todo4: study contango vs price changes! 
# todo5: trade algo module


futTab.loc[futTab.date==pd.to_datetime('2018-02-06')].close.plot()

"""
vixTab = ft.getVIX()
tab = futTab.set_index('date').join(vixTab.set_index('date'))

d = 5
T = 15
dT = 1
#fullTab['VIXdiff'] = fullTab.VIXClose.diff(d)
#fullTab['FUTdiff'] = fullTab.close.diff(d)
print tab.head()
#print tab.loc[(tab['daysToMat']<30) & (tab['daysToMat']>26) & (tab['close']>0)]
#tab_ = tab.loc[(60<=tab['daysToMat']) & (tab['daysToMat']<=30) & (tab['close']>0)]
tab_ = tab.loc[(tab['daysToMat'] <= T+dT) & (tab['daysToMat'] >= T-dT) & (tab['close']>0)]
tab_diff = tab_.diff(d)
tab_diff = tab_diff.dropna()
#tab_['VIXdiff'] = tab_.VIXClose.diff(d)
#tab_['FUTdiff'] = tab_.close.diff(d)

plt.plot(tab_diff.VIXClose, tab_diff.close,'o')
#plt.plot(tab_.VIXdiff, tab_.FUTdiff,'o')

#plt.show()

#plot linear fit
lm_original = np.polyfit(tab_diff.VIXClose, tab_diff.close, 1)
 
# calculate the y values based on the co-efficients from the model
r_x, r_y = zip(*((i, i*lm_original[0] + lm_original[1]) for i in tab_diff.VIXClose))
 
# Put in to a data frame, to keep is all nice
lm_original_plot = pd.DataFrame({
'dVIX' : r_x,
'dFUT' : r_y
})
plt.plot(lm_original_plot['dVIX'],lm_original_plot['dFUT'],'-')
plt.show()
"""
