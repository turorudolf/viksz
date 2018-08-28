import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print "reading data from disk.."

freq = '1day'
#freq = '10mins'

period = '10yr'
#period = '3M'

rootFolder = 'data/' + freq

instruments = ['VIX', 'V2TX']
data = pd.DataFrame({})
for instrument in instruments:
	fileName = rootFolder + '/' + instrument + '_' + period + '.csv'
	df = pd.read_csv(fileName,
		usecols=['date','open','close']).rename(
		columns={'date':'date', 'open':'open'+instrument, 'close':'close'+instrument}
		)
	#df['dateTime'] = df.date.map(str) + df.time.map(str)
	# todo: convert dateTime to right type
	#df = df.drop(['date','time'], axis=1)
	#df = df.set_index('dateTime')
	if data.empty:
		data = df
	else:
		data = data.join(df.set_index('date'), on='date')


#plt.plot( data.closeV2TX/data.openV2TX-1, data.closeVIX/data.openVIX-1,'o')

#data['V2TX_ret'] = data.closeV2TX.pct_change()
data['V2TX_ret'] = data.closeV2TX.diff(1)
#data['V2TX_ret'] = data.closeV2TX - data.openV2TX


#data['VIX_ret'] = data.closeVIX.pct_change()
data['VIX_ret'] = data.closeVIX.diff(1)
#data['VIX_ret'] = data.closeVIX- data.openVIX
day = 2
data['dVIX'] = data.closeVIX.shift(day) - data.closeVIX 
data['dVIX1'] = data.closeVIX.shift(2*day) - data.closeVIX.shift(day)


data = data.dropna()
print data.head()
x = data.V2TX_ret
#x = data.dVIX
y = data.VIX_ret
#y = data.dVIX1

plt.plot( x, y,'o')
#plt.plot(  data.closeVIX.pct_change(),data.closeV2TX.pct_change().shift(-1),'o')
#plt.plot( data.closeVIX/data.openVIX-1, data.closeV2TX.shift(-1)/data.openV2TX.shift(-1)-1, 'o')


#plot linear fit
lm_original = np.polyfit(x, y, 1)
 
# calculate the y values based on the co-efficients from the model
r_x, r_y = zip(*((i, i*lm_original[0] + lm_original[1]) for i in x))
 
# Put in to a data frame, to keep it all nice
lm_original_plot = pd.DataFrame({
'V2TX_ret' : r_x,
'VIX_ret' : r_y
})
plt.plot(lm_original_plot['V2TX_ret'],lm_original_plot['VIX_ret'],'-')
plt.show()
