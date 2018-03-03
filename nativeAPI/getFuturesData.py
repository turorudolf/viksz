import IBconn
import csv
import calendar

# map month's name to 2 digits number
months2Num = dict((v,str(k))  if k>9 else (v,'0'+str(k)) for k,v in enumerate(calendar.month_name))
expiries = []
with open("data/VIXmonthlyExp.txt") as csvDataFile:
    csvReader = csv.reader(csvDataFile, delimiter=' ')
    for row in csvReader:
        expiries.append(row[2] + months2Num[row[1]] + row[0])
fileName = 'data/VIXfuturesData.csv'
with open(fileName, "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(['expiry','date','open','high','low','close','volume'])
app = IBconn.createConnection("127.0.0.1", 7496, 2)
for expiry in expiries[:35]:
	print(expiry)
	ibcontract = IBconn.make_contract("VIX", "FUT", "CFE", expiry)
	ibcontract.includeExpired = True

	resolved_ibcontract = app.resolve_ib_contract(ibcontract)

	period_str = "10 Y"
	freq_str = '1 day'
	whatToShow = 'TRADES'

	historic_data = app.get_IB_historical_data(resolved_ibcontract, period_str, freq_str, whatToShow)

	#print(historic_data)
	with open(fileName, "a") as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			for line in historic_data:
				line_out = [expiry] + list(line)
				writer.writerow(line_out)
app.disconnect()
