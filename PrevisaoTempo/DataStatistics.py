# -*- coding: utf-8 -*-
'''
Created on Jun 27, 2016

@author: Nicoli
'''

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from unittest.mock import inplace

class DataStatistics(object):
    '''
    Pega arquivos do tipo .csv com dados acumulados anuais e diários de um mês e realiza estatísticas 
    '''

    def getAnnualDataFrame(self, month):
        return pd.read_csv('./Data/files/monthly/RainfallByYear/' + str(month) + 'a.csv', sep = r',')
     
    def getDailyDataFrame(self, month):
        return pd.read_csv('./Data/files/monthly/RainfallByDay/' + str(month) + 'd.csv', sep = r',')
    
    def getDailyMean(self, param):
        return self.DailyDataFrame[param].mean()
    
    def getAnnualMean(self, param):
        return self.AnnualDataFrame[param].mean()
    
    def getAnnualStd(self, param):
        #print(np.std(self.dataFrame[param]))
        return self.AnnualDataFrame[param].std()
    
    def getMeanStd(self, param):
        #print(np.std(self.dataFrame[param]))
        return self.DailyDataFrame[param].std()
    
    def getCI(self, param):
        '''
        http://hamelg.blogspot.com.br/2015/11/python-for-data-analysis-part-23-point.html
        The z-critical value is the number of standard deviations you'd have to go from the 
        mean of the normal distribution to capture the proportion of the data associated with 
        the desired confidence level. For instance, we know that roughly 95% of the data in a 
        normal distribution lies within 2 standard deviations of the mean, so we could use 2 as
        the z-critical value for a 95% confidence interval (although it is more exact to get 
        z-critical values with stats.norm.ppf().).

        '''

        size = self.AnnualDataFrame[param].size
        
        mean = self.getAnnualMean(param)
        

        std = self.getAnnualStd(param)
            
        zCritical = stats.norm.ppf(q = 0.95)
        zCritical = 0
        margin_of_error = zCritical * (std/math.sqrt(size))
        
        confidence_interval = (mean - margin_of_error, 
                               mean + margin_of_error)
        
        return(size, mean, std, zCritical, margin_of_error, confidence_interval)
    
   
    def writeInfo(self, param, month):
        
        with open('Data/files/statistics/statistics' + month + '.txt', 'w+') as file:
            file.write('\t\t\tStatistical Data\n\n')
            
            file.write('\t\tRAINFALL\n')
            
            (n, mean, std, zCritical, margin_of_error, confidence_interval) = self.getCI(param)
            file.write('\tn: '+ str(n) + '\n\tMean: '+ str(mean) + '\n\tstd: ' + str(std) + '\n\tz: ' +  str(zCritical) +  
                       '\n\tmargin of error: ' + str(margin_of_error) + '\n\tConfidence Interval: ' + str(confidence_interval))
            
            file.write('\n\tAHT Mean: ' + str(self.getDailyMean('AHT')))
            file.write('\n\tALT Mean: ' + str(self.getDailyMean('ALT')))
            file.write('\n\tARH Mean: ' + str(self.getDailyMean('ARH')))

    def setCorrData(self):
        dfcorr = {}
        #abrindo as dfs de todos os meses e colocando num dicionário
        for i in range(1, 13):
            stri = str(i)
            #criando uma chave do dicionário pra cada mês  
            dfcorr[i] = self.getAnnualDataFrame(stri)['RAINFALL']
            
        #criando um df
        dfcorr = pd.DataFrame(dfcorr)
        
        matCorr = dfcorr.corr()
        matCorr.sort(axis = 1, inplace=True)
        matCorr = matCorr.round(2)
        
        print(matCorr)
        return matCorr
        
           
   
    
    def writeCorrMatrix(self, df):
        '''Pearson Correlation Matrix
            This matrix takes for input all the dataframes in RainfallByYear.
            To generate this matrix, it was created a DataFrame containing 
            the accumulated rainfall in a month for each year.'''

        filename = './Data/files/statistics/PearsonCorrelationMatrix.csv' #a for annual
        with open(filename, 'w') as file:
            df.to_csv(file)
            
    def checkNaNData(self, month):
        totalPerDay = self.getAnnualDataFrame(month)
        nanRainfall = total.loc[total['RAINFALL'].isnull() == True]
        allNan = total.loc[total['RAINFALL'].isnull() == True and]
        
        
    def __init__(self, month):
        '''
        Constructor
        '''
        '''self.DailyDataFrame = self.getDailyDataFrame(month)
        self.AnnualDataFrame = self.getAnnualDataFrame(month)
        self.writeInfo('RAINFALL', month)
        '''