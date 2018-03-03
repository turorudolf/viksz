import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


 
df = pd.read_csv("data/VIXfuturesData.csv", dtype={'date': object, 'expiry': object})
# convert date and expiry to datetime
df['date'] = pd.to_datetime(df['date'])
df['expiry'] = pd.to_datetime(df['expiry'])
df.sort_values(['date', 'expiry'], inplace=True)
dates = df.date.unique()
#print(df[0:12])
# select rows with dates later than date1
#date1 = '2017-04-03'
date1 = dates[455]
#print(date1)
#mask = (df['date'] > date1)
#df_ = df[mask]
df['daysToMat'] = (df.expiry - df.date)
df.daysToMat = df['daysToMat'].apply(lambda x: x.days)



# plot forward curve
# df2.plot(x='expiry', y=['low','high','close'], style='-o')
# plt.show()
x = dates
y = []
tot = 1
start = np.nan
mindays = 0
for date in x:
	df2 = df.loc[df['date'] == date]
	days = df2.iloc[0].daysToMat
	if(len(df2.index) > 1 and days < 32):
		# todo: wtf is going on with iloc ??
		price = 0.5*(df2.iloc[0].close + df2.iloc[1].close )
		y.append( tot )
		if (np.isnan(start) and days > mindays):
			start = price
		if days == 0:
			tot = tot + (start - price)*min(0.2*tot, 1)
			start = np.nan
			print str(tot)
	else:
		y.append(np.nan)
print "total money="+str(tot)
plt.plot(x,y)
plt.show()

