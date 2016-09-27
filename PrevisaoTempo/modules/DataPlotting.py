# -*- coding: utf-8 -*-
'''
Created on 1 de jun de 2016

@author: nicoli-rna
'''
#import seaborn as sns
from pandas.tseries.index import DatetimeIndex

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class DataPlotting(object):
    '''
    classdocs
    '''
    def getMonthDataFrame(self, month):
        return pd.read_csv('../data/files/monthly/RainfallByDay' + str(month) + 'd.csv', sep = r',')
        
    
    '''def getRainfallTest(self):
        rainfallmean = 0
        for i in self.monthDataFrame['RAINFALL']:
            try:
                rainfallmean += i
            except:
                pass
        print(rainfallmean)
    '''
    
    def getRainfall(self, monthDataFrame):
        return monthDataFrame['RAINFALL'].mean()
    
    def getMonth(self, monthDataFrame):
        newMonthDataFrame = pd.DataFrame()

        #newMonthDataFrame.index = monthDataFrame['Date'].month
        newMonthDataFrame['RAINFALL'] = monthDataFrame['RAINFALL']
        newMonthDataFrame['MONTH'] = pd.DatetimeIndex(monthDataFrame["Date"], dayfirst=True).month
        return newMonthDataFrame
    
    def getMonthsRainfallDF(self):
        self.DataFrame = pd.DataFrame()
        for i in range(1,13):
            monthdf = self.getMonthDataFrame(i)
            newmonthdf = self.getMonth(monthdf)
            self.DataFrame = pd.concat([self.DataFrame,newmonthdf])
        print(self.DataFrame)
        
        #print(self.DataFrame.index)
        #print(self.DataFrame)

    
    def __init__(self):
        '''
        Constructor
        '''
        #self.getMonthsRainfall()
        #months = ['Janeiro', 'Fevereiro', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

        self.getMonthsRainfallDF()
        plt.clf()
        #self.DataFrame = self.DataFrame.groupby("MONTH").mean()
        #x = sns.barplot(x = self.DataFrame.index, y = 'RAINFALL', data = self.DataFrame, palette = 'Greys')
        x = sns.barplot(x="MONTH", y="RAINFALL", data=self.DataFrame,palette="Greys")
        x.set(xlabel='Meses', ylabel='Precipitação')
        sns.plt.savefig('../data/images/PrecxMesMedia.pdf')
        sns.plt.savefig('../data/images/PrecxMesMedia.png')
        plt.close()
        
         
        
        
        