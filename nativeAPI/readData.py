import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

month_codes = {}
month_names = {}
rootFolder = '/home/adamka/finance/data/vixfutures/'
fileName = rootFolder + 'monthCodes.txt'
with open(fileName) as csvDataFile:
    csvReader = csv.reader(csvDataFile, delimiter=',')
    for row in csvReader:
		month_codes[row[2]] = row[1]
		month_names[row[1]] = row[0]
print month_codes

fileName = rootFolder + 'VIXmonthlyExp.txt'
exp_tab = pd.read_csv(fileName, sep=' ', names=['day','month','year'])
print exp_tab.head()

yrs = [13, 14, 15, 16]
tabList = []
for yr in yrs:
	for month_code in month_codes.keys():
		fileName = rootFolder + '/20' + str(yr) +'/CFE_' + month_code + str(yr) + '_VX.csv'
		df = pd.read_csv(fileName,  usecols=['Trade Date','Futures', 'Open','High','Low','Close','Settle','Change','Total Volume'])
		tabList.append(df)
		#expiryDay = exp_tab.loc[(exp_tab.year == 2000+yr) & (exp_tab.month == month_names[month_codes[month_code]]) ].day
		#print 'day:' + str(expiryDay.iloc[0]) + ' month:' + month_codes[month_code]
tab = pd.concat(tabList)
tab = tab.rename(index=str, columns = {'Trade Date':'date', 'Futures':'expiry', 'Open':'open', 'High':'high', 'Low':'low', 'Close':'close','Settle':'settle','Change':'change','Total Volume':'volume'})
tab['date'] = tab['date'].apply(lambda x: x.replace("-",""))
print tab.loc[tab.date=='20130118']

def getExpiry(exp_str):
	res = exp_str.split(' ')
	month_code = res[0]
	year = int(res[2].replace(')',''))
	# too slow, replace this with a map?
	day_fr = exp_tab.loc[(exp_tab.year == year) & (exp_tab.month == month_names[month_codes[month_code]]) ].day
	day = day_fr.iloc[0]
	month = month_codes[month_code]
	return (str(year)+str(month)+str(day))
print "Getting expiries..."	
tab['expiry'] = tab['expiry'].apply(getExpiry)
print tab.loc[tab.date=='20130118']


# try a strategy todo: encapsulate this !!
df = tab

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
tot = tot0 = 1
start = np.nan
mindays = 3
cost = 0.0
def betFn(money):
	return min(0.4*money, 0.6)
for date in x:
	df2 = df.loc[df['date'] == date]
	days = df2.iloc[0].daysToMat
	if(len(df2.index) > 1 and days < 32):
		# todo: wtf is going on with iloc ??
		price = 0.3*df2.iloc[0].close + 0.7*df2.iloc[1].close 
		
		if (np.isnan(start) and days > mindays and not np.isnan(price)):
			start = price
			tot0 = tot
		if(not np.isnan(start)):
			tot = tot0 + ((start - price) / start * betFn(tot0))*(1 - cost)
		
		if days == 0:	
			print str(date) + " " + str(tot) + "  start=" + str(start) + " end=" + str(price)
			start = np.nan
	y.append(tot)
print "total money="+str(tot)
plt.plot(x,y)
plt.show()





