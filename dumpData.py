import tools.myClasses as tools
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from time import sleep, strftime
import datetime

spec_vxz = {'symbol':'VXZ', 
			'sec_type':'STK',
			'exch':'SMART',
			'prim_exch':'SMART',
			'curr':'USD',
			'trade_type':'TRADES'}
spec_vxx = {'symbol':'VXX', 
			'sec_type':'STK',
			'exch':'SMART',
			'prim_exch':'SMART',
			'curr':'USD',
			'trade_type':'TRADES'}
spec_vix = {'symbol':'VIX', 
			'sec_type':'IND',
			'exch':'CBOE',
			'prim_exch':'CBOE',
			'curr':'USD',
			'trade_type':'TRADES',
			'permission': 'CBOE Streaming Market Indexes'}
spec_vix3m = {'symbol':'VIX3M', 
			'sec_type':'IND',
			'exch':'CBOE',
			'prim_exch':'CBOE',
			'curr':'USD',
			'trade_type':'TRADES',
			'permission': 'CBOE Streaming Market Indexes'}
spec_vstoxx = {'symbol':'V2TX', 
			'sec_type':'IND',
			'exch':'DTB',
			'prim_exch':'DTB',
			'curr':'EUR',
			'trade_type':'TRADES',
			'permission': 'German ETFs and Indices'}
spec = spec_vix
contract = tools.instrument(spec)
#contract = tools.instrument('VIX', 'IND', 'CBOE', 'CBOE', 'USD', 'TRADES')


#freq = "30 mins"
freq = "10 mins"
#freq = "5 mins"
#freq = "1 hour"
#freq = "1 day"
period = '1 Y'
#period = '3 M'
filename = 'data/' + freq.replace(" ", "") + "/" + spec['symbol'] + '.csv'
handler = tools.connHandler(filename)

conn = ibConnection(host='127.0.0.1', port=7496, clientId=101)
# Register the response callback function and type of data to be returned
conn.register(handler.error_handler, message.Error)
conn.register(handler.save_order_id, 'NextValidId')
conn.register(handler.historical_data_handler, message.historicalData)
conn.connect()
#conn.reqHistoricalData(4001,contract,endTime,"90 D","1 min",tradeType,0,1)
tickerID = 0

conn.reqHistoricalData(tickerID, contract, '', period, freq, contract.trade_type, 1, 1)

print ("waiting a few sec...")
sleep(9)
handler.closeFile()
conn.disconnect()
print ("disconnected.")
