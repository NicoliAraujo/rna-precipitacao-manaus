# -*- coding: utf-8 -*-
'''
Created on 2 de mai de 2016

@author: Nicoli Araujo
'''
from DailyDataConfig import DailyDataConfig
from DataPlotting import DataPlotting
from DataStatistics import DataStatistics
from AnnualDataConfig import AnnualDataConfig 
from MatlabInputConfig import MatlabInputConfig
if __name__ == '__main__':
    a = DailyDataConfig('./Data/original/ClimateDataMao.txt') #transfere os dados da tabela no .txt pra 12 arquivos contendo os dados
    #de cada mês durante todos os anos
    #dataPlot = DataPlotting()
    #s = DataStatistics('1')
    for i in range (1,13):
        c = AnnualDataConfig(str(i), 'RAINFALL')
        #s = DataStatistics('1')
        
    
    #m = MatlabInputConfig()
    #m.makeMatlabInput(1,6)
    
    #s = DataStatistics('1')
    
    #s.writeCorrMatrix(s.setCorrData())
