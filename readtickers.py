'''
Created on 12 Feb 2020

@author: manojc
'''

#import requests
from six.moves import urllib
import json
import datetime
from datetime import datetime
from pytickersymbols import PyTickerSymbols
from astropy.table import index


# Headers to fake a user agent
_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

indices = [ 'AEX', 'BEL 20', 'CAC 40', 'DAX', 'DOW JONES', 'FTSE 100', 'IBEX 35', 'MDAX', 'NASDAQ 100', 'OMX Helsinki 15', 'OMX Helsinki 25', 'OMX Stockholm 30', 'S&P 100', 'S&P 500', 'SDAX', 'SMI', 'TECDAX' ]

class TickerData:
    '''
    classdocs
    '''
    def __init__(self, tickers, label):
        '''
        Constructor
        '''
        "Initialise from a sequence"
        self.tickers = tickers
        self.label = label
        self.myData = []
        self.stock_data = PyTickerSymbols()
        
    def get_ticker_data(self):
        return self.myData
        
    #@classmethod
    def from_filename(self, filename, label):
        "Initialise from a file"

        self.label = label
        with open(filename) as f:
            self.tickers = f.read().splitlines()
        
        self.__read_tickers(label)
        return self.tickers
    
    #@classmethod        
    def from_dict(self, tickerdict, label):
        "Initialise from a list"
        self.label = label
        self.tickers = tickerdict.items()
        return self.tickers
    
    #ß@classmethod
    def from_index(self, index):
        
        if not index in indices:
            print(f'Index {index} not found')
            return []
            
        self.label = index
        ticker_industries = [ [stock['symbol'], stock['industries']] for stock in self.stock_data.get_stocks_by_index(index)]
        print(ticker_industries)
        print(f'****** About to clean index {index }')
                
        ticker_industries = self.__cleanup_indices(index, ticker_industries)
        print(ticker_industries)        
        self.__read_tickers_from_list(index, ticker_industries)
        

    def __cleanup_indices(self, index, tickers):
        if index == 'FTSE 100':
            tickers = [ [ ticker[0][:-1], ticker[1] ] if ticker[0][-1:] == "." else ticker for ticker in tickers ]
            tickers = [ [ ticker[0][:-2], ticker[1] ] if ticker[0][-2:-1] == "." else ticker for ticker in tickers ]
    
            #Modify tickers to Add ".L" for FTSE Stocks
            tickers = [ [ ticker[0] + ".L", ticker[1] ] if ticker[0][-2:] != ".L" else ticker for ticker in tickers ]
            
            #Replace Anamoalies
            tickers = [ [ "FLTR.L", ticker[1] ] if ticker[0] == "PPB.L" else ticker for ticker in tickers ]
            tickers = [ [ "BT-A.L", ticker[1] ] if ticker[0] == "BT.L" else ticker for ticker in tickers ]
            
        elif index == 'S&P 500':
            #Replace Anamoalies
            tickers = [ [ ticker[0][:-2], ticker[1] ] if ticker[0][-2:] == ".L" else ticker for ticker in tickers ]
            #Replace Anamoalies
            tickers = [ [ "NLOK", ticker[1] ] if ticker[0] == "SYMC" else ticker for ticker in tickers ]
            tickers = [ [ "BKR", ticker[1] ] if ticker[0] == "BHGE" else ticker for ticker in tickers ]
            tickers = [ [ "LHX", ticker[1] ] if ticker[0] == "HRS" else ticker for ticker in tickers ]
            tickers = [ [ "PEAK", ticker[1] ] if ticker[0] == "HCP" else ticker for ticker in tickers ]
            tickers = [ [ "GL", ticker[1] ] if ticker[0] == "TMK" else ticker for ticker in tickers ]           
            tickers = [ ticker for ticker in tickers if ticker[0] != "APC" and ticker[0] != "RHT" ]
            
        elif index == 'DAX':
            tickers = [ [ ticker[0] + ".DE", ticker[1] ] if ticker[0][:-3] != ".DE" else ticker for ticker in tickers  ]
    
        elif index == 'NASDAQ 100':
            #Replace Anamoalies
            tickers = [ [ ticker[0][:-2], ticker[1] ] if ticker[0][-2:] == ".L" else ticker for ticker in tickers ]
            tickers = [ [ "TCOM", ticker[1] ] if ticker[0] == "CTRP" else ticker for ticker in tickers ]
            tickers = [ [ "NLOK", ticker[1] ] if ticker[0] == "SYMC" else ticker for ticker in tickers ]
        
        elif index == 'AEX':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".AS", ticker[1] ] if ticker[0][:-3] != ".AS" else ticker for ticker in tickers  ]
            tickers = [ [ "UNA.AS", ticker[1] ] if ticker[0] == "ULVR.AS" else ticker for ticker in tickers ]
            tickers = [ [ "REN.AS", ticker[1] ] if ticker[0] == "REL.AS" else ticker for ticker in tickers ]
        
        elif index == 'BEL 20':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".BR", ticker[1] ] if ticker[0][:-3] != ".BR" else ticker for ticker in tickers  ]
            tickers = [ [ "APAM", ticker[1] ] if ticker[0] == "APAM.BR" else ticker for ticker in tickers ]


        elif index == 'CAC 40':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".PA", ticker[1] ] if ticker[0][:-3] != ".PA" else ticker for ticker in tickers  ]
            tickers = [ [ "1BR1.F", ticker[1] ] if ticker[0] == "URW.PA" else ticker for ticker in tickers ]

        elif index == 'IBEX 35':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".MC", ticker[1] ] if ticker[0][:-3] != ".MC" else ticker for ticker in tickers  ]
            tickers = [ [ "MTS.MC", ticker[1] ] if ticker[0] == "MT.MC" else ticker for ticker in tickers ]
       
        elif index == 'MDAX':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".DE", ticker[1] ] if ticker[0][:-3] != ".DE" else ticker for ticker in tickers  ]
        
        elif index == 'OMX Helsinki 25':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".HE", ticker[1] ] if ticker[0][:-3] != ".HE" else ticker for ticker in tickers  ]
            tickers = [ [ "NRE1.VI", ticker[1] ] if ticker[0] == "NRE1V.HE" else ticker for ticker in tickers ]
        
        elif index == 'OMX Stockholm 30':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".ST", ticker[1] ] if ticker[0][:-3] != ".ST" else ticker for ticker in tickers  ]
            tickers = [ [ "TELIA1.HE", ticker[1] ] if ticker[0] == "TLS1V.ST" else ticker for ticker in tickers ]
            tickers = [ [ "NDA-FI.HE", ticker[1] ] if ticker[0] == "NDA-FI.ST" else ticker for ticker in tickers ]
            tickers = [ [ "ESSITY-B.ST", ticker[1] ] if ticker[0] == "ESSITY+B.ST" else ticker for ticker in tickers ]
        
        elif index == 'SDAX':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".DE", ticker[1] ] if ticker[0][:-3] != ".DE" else ticker for ticker in tickers  ]
            tickers = [ ticker for ticker in tickers if ticker[0] != "O1BC.DE" ]
        
        elif index == 'TECDAX':  
            #Modify tickers to Add ".AS" for AS Stocks
            tickers = [ [ ticker[0] + ".DE", ticker[1] ] if ticker[0][:-3] != ".DE" else ticker for ticker in tickers  ]
            tickers = [ ticker for ticker in tickers if ticker[0] != "O1BC.DE" ]            
        
        return tickers
                    
    def __read_tickers(self, indexLabel):
        for ticker in self.tickers:
            tickerItem = [ticker,""]
            tickerData = self.get_yahoo_quote(tickerItem, indexLabel)
            
            if tickerData !=  None:
                self.myData.append(tickerData)
 
    def __read_tickers_from_list(self, index, tickers):
        print("2: ", tickers)
        for ticker in tickers:    
            tickerItem=[]
            if type(ticker) == list: 
                tickerItem = ticker
            else:
                tickerItem = [ticker,""]
                
            tickerData = self.get_yahoo_quote(tickerItem, index)    
            
            if tickerData != None:
                self.myData.append(tickerData)
    
    
    def __convert_datetime_stamp(self, dictItems, field):
        if field in dictItems.keys():
            dictItems[field] = datetime.fromtimestamp(dictItems[field]).strftime("%Y-%m-%d %I:%M:%S")

    def get_yahoo_quote(self, ticker, label):  
        '''
        This function gets the ticker measures from Yahoo.
        '''
        param = dict()
        param['symbols'] = ticker[0]
        params = urllib.parse.urlencode(param)
        url = 'https://query1.finance.yahoo.com/v7/finance/{}?{}'.format('quote', params)
        print(url)
        req = urllib.request.Request(url, headers=_headers)

        # Perform the query
        # There is no need to enter the cookie here, as it is automatically handled by opener
        f = urllib.request.urlopen(req)
        values = json.load(f)
        print(values)

        try:
            data_json = values['quoteResponse']['result'][0]
        except IndexError:
            print(f'No quote found for SYMBOL:{ticker}')
            return None
            
        
        for field in ['regularMarketTime',
                      'preMarketTime',
                      'dividendDate',
                      'earningsTimestamp',
                      'earningsTimestampStart',
                      'earningsTimestampEnd' ]:
            self.__convert_datetime_stamp(data_json, field)
        
        #Add Indusstry as one column only for now    
        if type(ticker[1]) == list:
            data_json['industry'] = ticker[1]
            
        data_json['category'] = label
        ask_minus_bookValuePercent = 0.00
        
        if (("ask" in data_json) and ("bookValue" in data_json)):
            if float(data_json['ask']) != 0.0:            
                if (label == "FTSE100"):
                    ask_minus_bookValuePercent = (((data_json['ask']/100) - data_json['bookValue']) / (data_json['ask']/100)) *100
                elif label == "SP500" or label == "custom":
                    ask_minus_bookValuePercent = ((data_json['ask'] - data_json['bookValue']) / data_json['ask']) * 100

        data_json['askBookValueRatio'] = ask_minus_bookValuePercent

        if ("ask" in data_json and "fiftyTwoWeekLow" in data_json):
            if 'regularMarketPreviousClose' in data_json and data_json['ask'] == 0:
                data_json['Ask_52WLow'] = data_json['regularMarketPreviousClose'] - data_json['fiftyTwoWeekLow']
            else:
                data_json['Ask_52WLow'] = data_json['ask'] - data_json['fiftyTwoWeekLow']
        else:
            data_json['Ask_52WLow'] = 10000

        if ("bid" in data_json and "fiftyTwoWeekHigh" in data_json):
            if 'regularMarketPreviousClose' in data_json and data_json['ask'] == 0:
                data_json['Bid_52WHigh'] = data_json['regularMarketPreviousClose'] - data_json['fiftyTwoWeekHigh']
            else:
                data_json['Bid_52WHigh'] = data_json['bid'] - data_json['fiftyTwoWeekHigh']
        else:
            data_json['Bid_52WHigh'] = 10000

        mktVolvsDailyVol10DayPercent = 0.00
        
        if ("regularMarketVolume" in data_json) and ("averageDailyVolume10Day" in data_json):
            if data_json['regularMarketVolume'] != 0.0:
                mktVolvsDailyVol10DayPercent = ((data_json['regularMarketVolume'] - data_json['averageDailyVolume10Day'])/data_json['regularMarketVolume']) *100

        data_json['mktVolvsDailyVol10DayPercent'] = mktVolvsDailyVol10DayPercent

        mktVolvsDailyVol3MPercent = 0.00
        
        if ("regularMarketVolume" in data_json) and ("averageDailyVolume3Month" in data_json):
            if data_json['regularMarketVolume'] != 0.0:
                mktVolvsDailyVol3MPercent = ((data_json['regularMarketVolume'] - data_json['averageDailyVolume3Month']) /
                                            data_json['regularMarketVolume']) * 100

        data_json['mktVolvsDailyVol3MPercent'] = mktVolvsDailyVol3MPercent

        return data_json
