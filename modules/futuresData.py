import pandas as pd
import csv
import numpy as np

""" READING FUTURES DATA FROM CSV AND ADDING DAYS TO MATURITIES"""
""" OUTPUT IS PANDAS DATAFRAME                                      """
month_codes = {}
month_names = {}
# todo: make path a parameter?
rootFolder = '/home/adamka/finance/data/vixfutures/'
fileName = rootFolder + 'monthCodes.txt'
with open(fileName) as csvDataFile:
    csvReader = csv.reader(csvDataFile, delimiter=',')
    for row in csvReader:
        month_codes[row[2]] = row[1]
        month_names[row[0]] = row[1]
print "monthCodes OK.."

fileName = rootFolder + 'VIXmonthlyExp.txt'
exp_dict = {} # format: 'month year':'day'
with open(fileName, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            exp_dict[row[2]+'-'+month_names[row[1]]] = row[0]
print "expirations tab OK.."

def readFuturesData(expYrs):
    # todo:years should be trading dates not expiries!?
    # todo: this reads dates for expiries so for aerly dates there won't be 
    # all the futures listed !
    tabList = []
    for yr in expYrs:
        for month_code in month_codes.keys():
            if yr > 2009:
                yr_last2 = str(yr-2000)
            else:
                yr_last2 = '0' + str(yr-2000)
            fileName = rootFolder + '/' + str(yr) +'/CFE_' + month_code + yr_last2 + '_VX.csv'
            df = pd.read_csv(fileName,  usecols=['Trade Date','Futures', 'Open','High','Low','Close','Settle','Total Volume'])
            if yr < 2009:             
                df = df.apply(adjustPrices, axis=1)            
            tabList.append(df)
    tab = pd.concat(tabList)
    tab = tab.rename(index=str, columns = {'Trade Date':'date', 'Futures':'expiry', 'Open':'open', 'High':'high', 'Low':'low', 'Close':'close','Settle':'settle','Total Volume':'volume'})
    print "getting data OK.." 
    tab['expiry'] = tab['expiry'].apply(formatExp)
    print "formatting expiries OK.."
    tab['date'] = pd.to_datetime(tab.date)
    tab['date'] = tab['date'].dt.strftime('%Y-%m-%d')
    tab['daysToMat'] = map(lambda x,y: np.busday_count(x,y), tab.date, tab.expiry)
    tab['date'] = pd.to_datetime(tab.date)    
    tab['expiry'] = pd.to_datetime(tab['expiry'])
    #tab = tab.set_index('date')
    #tab['num'] = tab.apply(setOrdinal, axis=1)
    return tab

def getVIX():
    fileName = '/home/adamka/finance/data/vix/vixcurrent.csv'
    vix_tab = pd.read_csv(fileName, sep=',')
    vix_tab = vix_tab.rename(index=str, columns = {'Date':'date', 'VIX Open':'VIXOpen', 'VIX High':'VIXHigh', 'VIX Low':'VIXLow', 'VIX Close':'VIXClose'})
    vix_tab.set_index('date')
    return vix_tab
def formatExp(exp_str):
    res = exp_str.split(' ')
    month_code = res[0]
    year = res[2].replace(')','')
    if int(year) < 2000:
        year = '20'+year
    year_month = year  + '-' + month_codes[month_code]
    return  year_month + '-' + exp_dict[year_month]
def adjustPrices(row):
    if pd.to_datetime(row['Trade Date']) < pd.to_datetime('2007-03-26'):
        row.Open /= 10.
        row.Close /= 10.
        row.High /= 10.
        row.Low /= 10.
        row.Settle /= 10.
    return row
# todo: check why many num=1 missing 
def setOrdinal(row):
    #row.date = pd.to_datetime(row.date)
    #row.expiry = pd.to_datetime(row.expiry)
    if row.date.year == row.expiry.year:
        no = 1 + row.expiry.month - row.date.month
    else:
        no = 13 + row.expiry.month - row.date.month
    return no