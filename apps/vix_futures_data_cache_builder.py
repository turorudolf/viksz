# read daily VIX FUTURES data from CBOE 
# combines them to one big table and
# dump it into a CACHE

import modules.futuresData as ft
import numpy as np


# load data
futTab = ft.readFuturesData(range(2008, 2019))

futTab = futTab.sort_values(['date','expiry'])
dates = futTab.date.unique()
#futTab.loc[:,'slope'] = np.nan

#
# fix some data issues
#
# find rows with close==0
f = futTab.loc[futTab.close == 0]
# set zero close values as the mean of daily high and low
futTab.loc[f.index, 'close'] = 0.5*(futTab.iloc[f.index].high + futTab.iloc[f.index].low)
futTab.open = futTab.open.replace(0, np.nan)
futTab.close = futTab.close.replace(0, np.nan)
futTab.high = futTab.high.replace(0, np.nan)
futTab.low = futTab.low.replace(0, np.nan)
futTab.settle = futTab.settle.replace(0, np.nan)
# ffill + dropna ??

# todo: exclude first issues with big chg
# todo: fix numbering ! if there is not enough data no.1 will be assigned to a
# longer expiry!!

print "Setting ordinal numbers ..."
for date in dates:
    f = futTab[futTab.date==date]
    futTab.loc[futTab.date==date,'num'] = range(1, len(f) + 1)
    #futTab.loc[futTab.date==date,'slope'] = f.settle - f.settle.shift(1)
# keep only dates with at least 7 expiries
futTab = futTab.set_index(futTab.date)
gr = futTab.groupby(futTab.date).size()
futTab['cnt'] = gr[futTab.date]
futTab = futTab.loc[futTab.cnt > 6]
futTab = futTab.drop(['cnt'], axis=1)


futTab.to_csv('cache/vix_futures.csv',index=False)
print "Dumped to cache!"

# todo1: set multiplier before ~2008 it was *10 -- OK
# todo:1.1 fix indexing -- OK after loading from cache 
# todo:1.2 fix 0 prices
# todo: 1.3 dump data in a common cache OK
# todo2: set ordinal number of contract for each date! -- OK
# todo3: join w/ VIX tab and set slopes for front contracts!



#futTab.loc[futTab.date==pd.to_datetime('2018-02-06')].close.plot()





