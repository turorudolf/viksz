import pandas as pd
import os
import matplotlib.pyplot as plt

yrs = [2017, 2018]
per_str = '1H'
tabList = []
for yr in yrs:
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, '../data/CBOE/intra/'+per_str+'/'+str(yr)+'.csv')
	tabList.append(pd.read_csv(filename))
tab = pd.concat(tabList)
tab = tab.rename(columns={'TRADE_TIME':'time','CONTRACT_MONTH':'num', 'EXPR_DATE':'expr', 'TRADE_PRICE':'price'})
tab = tab.sort_values(['time'])
#tab = tab.set_index(tab.time)
F1 = tab.loc[tab.num==1][['time','price']]
F2 = tab.loc[tab.num==2][['time','price']]
print F1.describe()
#print F2.price-F1.price
plt.plot(F1.price)
plt.show()

