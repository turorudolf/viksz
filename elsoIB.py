from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from time import sleep, strftime
import datetime
import matplotlib.pyplot as plt


def make_contract(symbol, sec_type, exch, prim_exch, curr):
    Contract.m_symbol = symbol
    Contract.m_secType = sec_type
    Contract.m_exchange = exch
    Contract.m_primaryExch = prim_exch
    Contract.m_currency = curr
    return Contract
vec = []
tickerID = 0

def historical_data_handler(msg):
    # The response data callback function
    print (msg.reqId, msg.date, "open:" + str(msg.open), "close:" + str(msg.close), msg.high, msg.low)
    #print(msg)
    #if(msg.close > 0):
	#	vec.append(msg.close)
	#print(msg)
def error_handler(msg):
    print(msg)
def save_order_id(msg):
    print('Next Valid ID is ' + str(msg.orderId))
    tickerID = msg.orderId

#contract = make_contract('TSLA', 'STK', 'SMART', 'SMART', 'USD')
#contract = make_contract('VIX', 'IND', 'CBOE', 'CBOE', 'USD');tradeType = 'TRADES'
#contract = make_contract('SPX', 'IND', 'CBOE', '', 'USD');tradeType = 'TRADES'
contract = make_contract('EUR', 'CASH', 'IDEALPRO', 'IDEALPRO', 'USD');tradeType = 'BID'
#contract = make_contract('VIX', 'FUT', 'CFE', 'CFE', 'USD');tradeType = 'TRADES'
#contract = make_contract('VINIX', 'FUND', 'FUNDSERV', 'FUNDSERV', 'USD');tradeType = 'TRADES'
#contract.m_expiry = '20180321'
#contract = make_contract('VX09G8', 'FUT', 'CBOE', 'CBOE', 'USD')
"""
contract = Contract()
contract.symbol = "VINIX"
contract.secType = "FUND"
contract.exchange = "FUNDSERV"
contract.currency = "USD"
"""

conn = ibConnection(host='127.0.0.1', port=7496, clientId=100)

# Register the response callback function and type of data to be returned


conn.register(error_handler, message.Error)
conn.register(save_order_id, 'NextValidId')
conn.register(historical_data_handler, message.historicalData)
#conn.register(historical_data_handler)

queryTime = (datetime.datetime.today() - datetime.timedelta(days=20)).strftime("%Y%m%d %H:%M:%S")

endTime = strftime('%Y%m%d 17:00:00')




conn.connect()
#conn.reqHistoricalData(4001,contract,endTime,"90 D","1 min",tradeType,0,1)
conn.reqHistoricalData(tickerID, contract, '', '20 W', '1 hour', tradeType, 1, 1)
#conn.reqHistoricalData(tickerId=tickerID,contract=contract,endDateTime=strftime('%Y%m%d 17:00:00'),durationStr='50 D',barSizeSetting='10 mins',whatToShow=tradeType,useRTH=0,formatDate=1)



print ("waiting a few sec...")

sleep(2)
conn.disconnect()
print ("disconnected.")
#plt.plot(vec)
#plt.show()
