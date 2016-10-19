'''
Created on 18 de out de 2016

@author: pibic-elloa-nicoli
'''
from FromTxtToCSV import Rainfall2008_2015


if __name__ == '__main__':
    FILEPATH1 = '../data/files/original/other/chuvaMensal2008-2015.txt'
    CHUVA2008_2015 = Rainfall2008_2015(FILEPATH1)
    CHUVA2008_2015.set_months_data_frame()
    CHUVA2008_2015.months_data_frame.index.name = 'Year'
    FILEPATH2 = '../data/files/original/csv/rainfall_2008_2015.csv'
    
    print(CHUVA2008_2015.months_data_frame)
    CHUVA2008_2015.months_data_frame.to_csv(FILEPATH2, sep=r',', decimal=2)
    