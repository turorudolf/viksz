from ib.ext.Contract import Contract
import csv

class instrument(Contract):
    def __init__(self, spec):
        Contract.m_symbol = spec['symbol']
        Contract.m_secType = spec['sec_type']
        Contract.m_exchange = spec['exch']
        Contract.m_primaryExch = spec['prim_exch']
        Contract.m_currency = spec['curr']
        self.trade_type = spec['trade_type']
        Contract.m_localSymbol = spec['localSymbol']
        #Contract.m_lastTradeDateOrContractMonth = spec['lastTradeDateOrContractMonth']
# connection handlers
class connHandler():
    def __init__(self, filename):
        self.filename = filename
        self.outfile = open(self.filename, 'w')
        self.writer = csv.writer( self.outfile )
        self.writer.writerow(['date','time','open','high','low','close','volume'])
    def historical_data_handler(self, msg):
        # The response data callback function
        date_time = msg.date.split("  ")
        print(msg)
        #print (date_time[0], date_time[1], msg.open,  msg.high, msg.low, msg.close, msg.volume)
        #self.writer.writerow([date_time[0], date_time[1], msg.open,  msg.high, msg.low, msg.close, msg.volume])
    def error_handler(self,msg):
        print(msg)
    def save_order_id(self,msg):
        print('Next Valid ID is ' + str(msg.orderId))
        tickerID = msg.orderId
    def closeFile(self):
        self.outfile.close()


