

import pandas as pd
import numpy as np
import urllib.request
import csv
from dateutil import parser

urlInputs = ['http://www.bcb.gov.br/pec/Indeco/Ingl/ie5-24i.xlsx', 'http://www.bcb.gov.br/pec/Indeco/Ingl/ie5-26i.xlsx']
inputFiles = []


class timeSeriesTest:
	'''Initializer method for timeSeriesTest class
	@parms: url- url for data
	@params excelInputFile- optional, not used in this code however
	'''
    def __init__(self, url='', excelInput=''):
        self.url = url
        self.excelInput = excelInput
        self.currentDate = ''
        self.df = ''
        self.outputList = []
		##Downloading the input files using the request.urlretrieve
        print("Downloading inputs from", url)
        inputFiles.append(url.split('/')[-1])
        urllib.request.urlretrieve(url, filename=url.split('/')[-1])##Extracting the part after the last / which is the file name
        
    '''
	Loads the timeseries data into pandas dataframe for further processing
	'''
    def loadTimeSeriesData(self):
		# This functions loads timeseries data
        print("Loading time series data from", self.url)
        
        if self.excelInput == 'ie5-24i.xlsx':
            self.outputList = []
            self.df = pd.read_excel(self.excelInput, headers=None)
            parsedDate = parser.parse('{}/{}/{}'.format(self.df.iloc[-7][0], self.df.iloc[-7][1][0:3], self.df.iloc[-11][1]))
            self.currentDate = '{}/{}/{}'.format(parsedDate.month, parsedDate.day, parsedDate.year)
            self.currentDate1 = '{}/{}/{}'.format(parsedDate.month, parsedDate.day-1, parsedDate.year)
            self.currentDate2 = '{}/{}/{}'.format(parsedDate.month, parsedDate.day-2, parsedDate.year)
            #print(self.currentDate)
            self.outputList.append([self.currentDate] + self.df.iloc[-11][2:].values.tolist())
            self.outputList.append([self.currentDate1] + self.df.iloc[-12][2:].values.tolist())
            self.outputList.append([self.currentDate2] + self.df.iloc[-13][2:].values.tolist())
            
        else:
            self.outputList = []
            self.df = pd.read_excel(self.excelInput, headers=None)
			##The below two lines fetches the date part, navigating through the excel input to get the current date
            parsedDate = parser.parse(self.df.columns[2])
            self.currentDate = '{}/{}/{}'.format(parsedDate.month, 1, parsedDate.year)
            self.outputList.append(self.currentDate)
            self.outputList.append(self.df.iloc[-6].values[-1])
	'''
	Writes the output information to the output files bcb_output_1 and bcb_output_2 depending 
	on the url in the context
	'''
    
    def writeOutputData(self):
        if self.excelInput == 'ie5-24i.xlsx':
            with open('bcb_output_1.csv', 'a') as outputFile1:
                for _ in self.outputList:
                    wr = csv.writer(outputFile1, quoting=csv.QUOTE_NONE)
                    wr.writerow(_)
        
        else:
            with open('bcb_output_2.csv', 'a') as outputFile2:
                wr2 = csv.writer(outputFile2, quoting=csv.QUOTE_ALL)
                wr2.writerow(self.outputList)
            




    
def main():
    seriesObj1 = timeSeriesTest(url=urlInputs[0], excelInput='ie5-24i.xlsx')
    seriesObj2 = timeSeriesTest(url=urlInputs[1], excelInput='ie5-26i.xlsx')
    inputFiles.clear()
    seriesObj1.loadTimeSeriesData()
    seriesObj2.loadTimeSeriesData()
    seriesObj1.writeOutputData()
    seriesObj2.writeOutputData()

if __name__ == '__main__':
    main()