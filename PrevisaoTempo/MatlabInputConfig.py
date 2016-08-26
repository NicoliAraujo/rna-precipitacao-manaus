# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2016

@author: Nicoli
'''
import pandas as pd
import numpy as np
class MatlabInputConfig(object):
    '''
    REAJUSTAR PARA OUTROS MESES
    '''
    def getMontshData(self, month, amtPastMonths):
        dictMonthsData = {}
        '''
        monthlist = []
        for i in range(0, amtPastMonths):
            if i!=12:
                monthlist.append(12-i)
            elif 12 not in monthlist:
                monthlist.append(12)
        '''
        '''if month not in monthlist:
            monthlist.append(month)'''
        monthlist = [10, 11, 12, 4, 5, 2]    
        print(monthlist)
        
        for currMonth in monthlist:
            dictMonthsData[currMonth] = pd.read_csv('./Data/files/monthly/RainfallByYear/' + str(currMonth) + 'a.csv', sep = r',')
        dictMonthsData['Output'] = pd.read_csv('./Data/files/monthly/RainfallByYear/' + str(month) + 'a.csv', sep = r',')
        #print(dictMonthsData[1]['Year'])
        return dictMonthsData
    
    def makeMatlabInput(self, month, amtPastMonths):
        dictMonhtsData = self.getMontshData(month, amtPastMonths)
        
        dictdf = {}

        
        
        #colocando cada .csv em uma chave do dicionario, já excluindo os dados de 2010 que são um input sem output pra 2011
        for key in dictMonhtsData:
            if key!='Output':
                dictdf[key] = dictMonhtsData[key]['RAINFALL'].loc[dictMonhtsData[key]['Year']!=2010].values[:]
        
      
        
        #excluindo o primeiro rainfall, pq não tem como a rede advinhar esse (é um output sem input)
        dictdf['Output'] = dictMonhtsData['Output']['RAINFALL'].loc[dictMonhtsData['Output']['Year']!=1970].values[:]
        
        
        #criando os índices
        #os números correspondem ao ano que se quer adivinhar.        
        
        myindex = list(range(1971, 2011))
        df = pd.DataFrame(dictdf, index=myindex)
        #df = pd.DataFrame(dictdf)
        #organizando a ordem das colunas
        dfcolumns = df.columns.tolist()
        dfcolumns.remove('Output')
        dfcolumns.sort()
        dfcolumns.append('Output')
        df = df[dfcolumns]
        
        print(df)
        self.save(df, month, amtPastMonths)
     
    def save(self, df, month, amtPastMonths):
        filename = './Data/files/MatlabInput/' + str(month) + '_PCorr_'+ str(amtPastMonths) + 'inputs' + '.csv'
        with open(filename, 'w') as file:
            df.to_csv(file)
        
    def __init__(self):
        '''
        Constructor
        '''
        