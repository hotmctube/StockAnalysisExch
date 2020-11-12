'''
Created on 12 Feb 2020

@author: manojc
'''
from datetime import datetime
import numpy as np
import pandas as pd
import readtickers as rd
from abc import ABC, abstractmethod
from readtickers import TickerData

report_types = [ 'mktVolvsDailyVol10DayPercent',
'fiftyDayAverageChangePercent',
'twoHundredDayAverageChangePercent',
'dividendDate',
'trailingAnnualDividendRate',
'trailingPE',
'bookValue',
'priceToBook',
'askBookValueRatio',
'Ask_52WLow',
'Bid_52WHigh',
'regularMarketChangePercent' ]

class Data(ABC):
    
    @abstractmethod
    def create_data_frame(self): pass

class StockData(Data):
    '''
    This class holds stock information that we want to capture, pass and distribute for manipulation
    '''
    def __init__(self, outputDir):
        '''
        Constructor
        '''
        self.ticker_info = []
        self.data = pd.DataFrame
        self.tickerData = TickerData([], "")
        self.strDateTimeValue = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.fileSuffix = self.strDateTimeValue +".csv"
        self.outputDir = outputDir
        self.weights = {}
            
    def __call__(self):
        print("Called StockData()")
        
    def load_tickers_from_file(self, customFile, label):
        self.tickerData.from_filename(customFile, label)
        
    def load_tickers_from_exch_list(self, exchanges): 
        if len(exchanges) != 0:
            if ("ALL" in exchanges):
                for index in rd.indices:
                    self.tickerData.from_index(index)
            else:
                for index in exchanges:
                    self.tickerData.from_index(index)
    
    def create_data_frame(self):        
        myData = self.tickerData.get_ticker_data()
        print(myData)
        self.data = pd.DataFrame.from_dict(myData)
        self.data.pop('language') 
        self.data.pop('region')
        self.data.pop('triggerable')
        
    def rearrange_df_cols(self):
        cols = list(self.data)
        i = 0
        cols.insert(i, cols.pop(cols.index('symbol')))
        i += 1
        cols.insert(i, cols.pop(cols.index('category')))
        i += 1
        #cols.insert(i, cols.pop(cols.index('industry')))
        #i += 1
        cols.insert(i, cols.pop(cols.index('longName')))
        i += 1
        cols.insert(i, cols.pop(cols.index('shortName')))
        i += 1
        cols.insert(i, cols.pop(cols.index('marketCap')))
        i += 1
        cols.insert(i, cols.pop(cols.index('currency')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketChangePercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketChange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketPreviousClose')))
        i += 1
        cols.insert(i, cols.pop(cols.index('ask')))
        i += 1
        cols.insert(i, cols.pop(cols.index('bid')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekLow')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekHigh')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketDayRange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('askSize')))
        i += 1
        cols.insert(i, cols.pop(cols.index('bidSize')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketPrice')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketTime')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketOpen')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketDayHigh')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketDayLow')))
        i += 1
        cols.insert(i, cols.pop(cols.index('mktVolvsDailyVol10DayPercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('mktVolvsDailyVol3MPercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('regularMarketVolume')))
        i += 1
        cols.insert(i, cols.pop(cols.index('averageDailyVolume10Day')))
        i += 1
        cols.insert(i, cols.pop(cols.index('averageDailyVolume3Month')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyDayAverageChangePercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyDayAverageChange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyDayAverage')))
        i += 1
        cols.insert(i, cols.pop(cols.index('twoHundredDayAverageChangePercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('twoHundredDayAverageChange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('twoHundredDayAverage')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekLowChange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekLowChangePercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekRange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekHighChange')))
        i += 1
        cols.insert(i, cols.pop(cols.index('fiftyTwoWeekHighChangePercent')))
        i += 1
        cols.insert(i, cols.pop(cols.index('dividendDate')) if "dividendDate" in cols else "" )
        i += 1
        cols.insert(i, cols.pop(cols.index('earningsTimestamp')))
        i += 1
        cols.insert(i, cols.pop(cols.index('earningsTimestampStart')))
        i += 1
        cols.insert(i, cols.pop(cols.index('earningsTimestampEnd')))
        i += 1
        cols.insert(i, cols.pop(cols.index('trailingAnnualDividendRate')))
        i += 1
        cols.insert(i, cols.pop(cols.index('trailingPE')))
        i += 1
        cols.insert(i, cols.pop(cols.index('forwardPE')))
        i += 1
        cols.insert(i, cols.pop(cols.index('trailingAnnualDividendYield')))
        i += 1
        cols.insert(i, cols.pop(cols.index('epsTrailingTwelveMonths')))
        i += 1
        cols.insert(i, cols.pop(cols.index('epsForward')))
        i += 1
        cols.insert(i, cols.pop(cols.index('sharesOutstanding')))
        i += 1
        cols.insert(i, cols.pop(cols.index('bookValue')))
        i += 1
        cols.insert(i, cols.pop(cols.index('forwardPE')))
        i += 1
        cols.insert(i, cols.pop(cols.index('priceToBook')))
        i += 1
        cols.insert(i, cols.pop(cols.index('askBookValueRatio')))
        i += 1
        cols.insert(i, cols.pop(cols.index('Ask_52WLow')))
        i += 1
        cols.insert(i, cols.pop(cols.index('Bid_52WHigh')))
        i += 1
        cols.insert(i, cols.pop(cols.index('quoteType')))
        i += 1
        cols.insert(i, cols.pop(cols.index('quoteSourceName')) if "quoteSourceName" in cols else "" )
        i += 1
        cols.insert(i, cols.pop(cols.index('financialCurrency')))
        i += 1
        cols.insert(i, cols.pop(cols.index('marketState')))
        
        #Moved WT_Total to end of list if exists
        cols.insert(len(self.data.columns), cols.pop(cols.index('WT_Total')) if "WT_Total" in cols else "" )        
        self.data = self.data.reindex(columns=cols)
        self.data = self.data.drop_duplicates(subset='symbol', keep='first')
        
    def __output(self, filename):
        if len(self.outputDir) > 0:
            filename = self.outputDir + '/' + filename
        
        print(f'FILENAME TO OUTPUT {filename}')
        self.data.to_csv(filename, index=None, header=True)

    def rowIndex(self, row):
        return row.name
    
    def generate_weights(self, dictWeightCols, listTotalWeightCols, sortColumn):
        #if sortColumn is blank then sort by the total aggregated weight column WT_Total
        df_len = len(self.data)
 
        firstKey = True       
        for key in dictWeightCols:
            if len(key) > 0 and key in self.data.columns:
                self.data = self.data.sort_values(by=key,ascending=dictWeightCols[key])
            
            weights = []
            
            for i in range(df_len):
                weights.append((df_len - i)/df_len)
            
            if len(key) > 0:
                self.data[f'WT_{key}'] = weights
        
            if key in listTotalWeightCols:
                if firstKey == True:
                    self.data['WT_Total'] = self.data[f'WT_{key}']
                    firstKey = False
                else:
                    self.data['WT_Total'] *= self.data[f'WT_{key}']
         
        if len(sortColumn) > 0:
            if sortColumn in self.data:
                self.data = self.data.sort_values(by=sortColumn,ascending=False)
        else:
            if 'WT_Total' in self.data.columns:
                self.data = self.data.sort_values(by='WT_Total',ascending=False)
            else:
                print(f'Could not find {sortColumn}')
              
    def gen_report(self, prefix):
        strFilename = f'{prefix}_{self.fileSuffix}'
        self.rearrange_df_cols()
        self.__output(strFilename)
          
    def generate_report(self, prefix, sortField, ascending, lastReport):    
        if len(sortField) > 0 and sortField in self.data.columns:
            self.data = self.data.sort_values(by=sortField,ascending=ascending)
         
        iWeight = []
        df_len = len(self.data)
        
        for i in range(len(self.data)):
            iWeight.append((df_len-i)/df_len)
            
        if len(sortField) > 0:
            self.data[f'WT_{sortField}'] = iWeight
        
        if lastReport == True:
            self.data['WT_Total'] = self.data['WT_trailingAnnualDividendRate'] * \
                                    self.data['WT_trailingPE'] * \
                                    self.data['WT_bookValue'] * \
                                    self.data['WT_priceToBook'] * \
                                    self.data['WT_askBookValueRatio'] * \
                                    self.data['WT_Ask_52WLow']
                                                    
            strFilename = f'{prefix}_{self.fileSuffix}'
            self.rearrange_df_cols()
            self.__output(strFilename)
