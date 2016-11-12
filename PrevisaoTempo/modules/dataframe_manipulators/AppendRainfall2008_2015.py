'''
Created on 18 de out de 2016

@author: pibic-elloa-nicoli
'''
from FromTxtToCSV import Rainfall2008_2015
import pandas as pd

if __name__ == '__main__':
    FILEPATH1 = '../../data/files/original/other/chuvaMensal2008-2015.txt'
    CHUVA2008_2015 = Rainfall2008_2015(FILEPATH1)
    CHUVA2008_2015.set_months_data_frame()
    CHUVA2008_2015.months_data_frame.index.name = 'Year'
    FILEPATH2 = '../../data/files/original/csv/rainfall_2008_2015.csv'
    
    #print(CHUVA2008_2015.months_data_frame)
    CHUVA2008_2015.months_data_frame.to_csv(FILEPATH2, sep=r',', decimal=2)
    
    FILEPATH4 = '../../data/files/original/csv/rainfall1925_2007.csv'
    rainfall_1925_2007 = pd.read_csv(FILEPATH4, sep=r',', index_col=0)
    FILEPATH3 = '../../data/files/original/csv/rainfall_1925_2015.csv'
    #print(rainfall_1925_2007)
    #print(CHUVA2008_2015.months_data_frame)
    rainfall_1925_2015 = pd.concat([rainfall_1925_2007,CHUVA2008_2015.months_data_frame])
    #print(rainfall_1925_2015)
    #print(rainfall_1925_2015.dtypes)
    rainfall_1925_2015.to_csv(FILEPATH3, sep=r',')