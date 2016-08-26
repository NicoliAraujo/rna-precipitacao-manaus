# -*- coding: utf-8 -*-
'''
Created on 29 de jun de 2016

@author: projeto
'''
import pandas as pd
import numpy as np
class AnnualDataConfig(object):
    '''
    Vem diretamente do .csv original. 
    Gera um arquivo:
    
        Year    RAINFALL
    1970    98.80000000000001
    1971    182.29999999999998
    1972    94.2
    1973    181.8
    1974    24.4
    1975    55.0
    1976    123.0
    1977    190.79999999999995
    1978    115.6
    1983    195.8

    para cada mês.
    Os números são somatórios do quanto choveu em cada mês de cada ano.
    Descarta os nans.
    '''

    def getMonthDataFrame(self):
        return pd.read_csv('./Data/files/monthly/RainfallByDay/' + str(self.month) + 'd.csv', sep = r',')
    
    def setDataFrame(self, df):
        dflist = [[],[]]
    
        for i in range(0, df['Date'].size):
            dflist[0].append(int(df['Date'][i][-4:]))
            dflist[1].append(df[self.param][i])
        newdf = pd.DataFrame ( {'Year': dflist[0],
                                self.param : dflist[1] } )
        return newdf
    
    def accumParam(self, df):
        acParam = {}
        
        for i in range(0, df['Year'].size):
            key = df['Year'][i]
            value = df[self.param][i]
            if (key not in acParam) :
                acParam[key] = value
            elif (key in acParam) :
                acParam[key] +=value
     
        acParamlist = [[],[]]
        for i in acParam:
            acParamlist[0].append(i)
            acParamlist[1].append(acParam[i])

        newdf = pd.DataFrame( {self.param: acParamlist[1]}, index = acParamlist[0] )
        
        newdf.index.name = 'Year'
        
        newdf = newdf.loc[newdf.index <=2010]
        
        newdf = newdf.loc[newdf['RAINFALL'].notnull() == True]
        
        newdf.sort_index(inplace = True)
        
        return newdf
    
    def setCSV(self, df):
        filename = './Data/files/monthly/RainfallByYear/' + self.month + 'a.csv'
        with open(filename, 'w') as file:
            df.to_csv(file)
            
    def __init__(self, month, param):
        self.param = param
        self.month = month
        self.setCSV(self.accumParam(self.setDataFrame(self.getMonthDataFrame())))