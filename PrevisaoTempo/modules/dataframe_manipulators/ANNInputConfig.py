# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2016

@author: Nicoli
'''
import numpy as np
import pandas as pd


class ANNInput():
    '''Classe que cria os arquivos que servirão de entrada para a rede neural. 
    Os data frames são compostos de: 
    1) rainfall_month | rainfall/tsa/ninos_[month:month-time_gap]
    '''
    def open_join_data_frame(self):
        '''abre o df com todos os dados'''
        path = '../../data/files/original/AllData.csv'
        return pd.read_csv(path, sep=r',', index_col=0).round(2)

    def get_months(self):
        '''retorna uma lista com um número time_gap de meses que vão de
        month - 1 até month - timegap, circularmente
        '''
        all_months = [i for i in range(1,13)]
        return [all_months[int(self.month) - i] for i in range(2, self.time_gap + 2)]

    def set_month_data(self):
        '''pegar: rainfall daquele mês e
        rainfall, tsa, nino12, nino 3, nino34 e nino4 dos 6 meses antes'''
        self.month_data['rainfall_' + self.month] = self.join_df['rainfall_' + self.month]

        for name in self.join_df.columns:
            if int(name[-2:]) in self.get_months():
                self.month_data[name] = self.join_df[name]
        
    def __init__(self, month, time_gap):
        self.month = month
        self.time_gap = time_gap
        self.join_df = self.open_join_data_frame()
        self.month_data = pd.DataFrame()

    def save(self, folder):
        filename = '../../data/files/anninputs/' + folder + '/' + self.month + '_'+ str(self.time_gap) + '.csv'
        with open(filename, 'w') as file:
            self.month_data.to_csv(file, sep = r',')
    
    def normalize_data(self):
        df = self.month_data
        
        for name in self.month_data.columns:
            #print(name[:-3])
            if name[:-3] != 'tsa':
                #print(self.join_df[name].sum())
                #print(df[name])
                df[name] = self.month_data[name]/self.month_data[name].abs().sum()
                #print(df[name])
                self.month_data = df
        #print(self.join_df)
        
                
if __name__ == '__main__':
    keylist = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for month in keylist:
        ANNINPUT = ANNInput(month, 6)
        ANNINPUT.set_month_data()
        ANNINPUT.save('nonnormalizedinputs')
        ANNINPUT.normalize_data()
        #print(ANNINPUT.month_data)
        ANNINPUT.save('normalizedinputs')