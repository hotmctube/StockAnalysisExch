'''
Created on 13 Feb 2020

@author: manojc
'''
import stockdata as sd
from pytickersymbols import PyTickerSymbols

#Define Output Directory Path for output
outputDir = '/Users/manojc/Projects/StockAnalysis2'
#Define Location of custom tickers to be included in the output
customFile = '/Users/manojc/eclipse-workspace/StockAnalysisExch/tickers.txt'
#Define Exchanges from which to pull trade tickers
exchanges = [ 'AEX', 'BEL 20', 'CAC 40', 'DAX', 'DOW JONES', 'FTSE 100', 'IBEX 35', 'MDAX', 'NASDAQ 100', 'OMX Helsinki 25', 'S&P 100', 'S&P 500', 'SDAX', 'SMI', 'TECDAX' ]

stockdata = sd.StockData(outputDir)
stockdata.load_tickers_from_file(customFile,'Custom')
stockdata.load_tickers_from_exch_list(exchanges)
stockdata.create_data_frame()

weightColumns = { 'mktVolvsDailyVol10DayPercent':False,
                  'fiftyDayAverageChangePercent':False,
                  'twoHundredDayAverageChangePercent':False,
                  'trailingAnnualDividendRate':False,
                  'dividendDate':False,
                  'trailingAnnualDividendRate':False,
                  'trailingPE':True, 
                  'bookValue':False, 
                  'priceToBook':True, 
                  'askBookValueRatio':True, 
                  'Ask_52WLow':True,
                  'Bid_52WHigh':True,
                  'regularMarketChangePercent':True }

totalWeightColumns = [ 'trailingAnnualDividendRate', 
                       'trailingPE', 
                       'priceToBook', 
                       'askBookValueRatio', 
                       'Ask_52WLow' ]

sortColumn = {}
stockdata.generate_weights(weightColumns, totalWeightColumns, sortColumn)

stockdata.gen_report('stock_analysis_by_weight')


if __name__ == '__main__':
    pass
