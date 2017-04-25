'''
Created on 26 de set de 2016

@author: pibic-elloa-nicoli
'''
import pandas as pd
import numpy as np

class Anomaly(object):
    '''
    classdocs
    '''
    def get_original_data(self):
        filepath = '../../data/files/original/csv/' + self.name + '.csv'
        return pd.read_csv(filepath, sep=r',', index_col='Year')

    def set_anomaly_df(self):
        self.anomaly_df = self.df - self.df.mean()

    def save_df_to_csv(self):
        filename = '../../data/files/anomalydata/' + self.name + '.csv'
        with open(filename, 'w') as file:
            self.anomaly_df.round(2).to_csv(file)

    
    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.df = self.get_original_data()
        self.mean = 0
        self.anomaly_df = pd.DataFrame()

class Correlacao():
    def get_normalized_data(self):
        filepath = '../../data/files/original/csv/' + self.name + '.csv'
        return pd.read_csv(filepath, sep=r',', index_col='Year')
    
    def get_corr_dataset(self, month):
        col_list = self.get_col_list(month)
        self.corr_dataset = self.df[col_list]
        self.corr_dataset=pd.DataFrame(self.corr_dataset.corr()['rainfall_'+month]).transpose()
        self.corr_dataset.index = ['Valor']
        self.corr_dataset=self.corr_dataset.transpose()
        self.corr_dataset['Relacao'] = 'Neutra'
        print(self.corr_dataset.loc[self.corr_dataset['Valor']>0]['Relacao'])
        #print(self.corr_dataset.loc[:,'rainfall_01'])
        self.corr_dataset.loc[self.corr_dataset['Valor']>0,'Relacao'] = 'Positiva'
        self.corr_dataset.loc[self.corr_dataset['Valor']<0,'Relacao'] = 'Negativa'
        
        self.corr_dataset['Valor'] = abs(self.corr_dataset['Valor'])
        self.corr_dataset = self.corr_dataset.sort_values('Valor',ascending=False)
        print(self.corr_dataset)
    def get_col_list(self, month):
        col_list = [col for col in self.df.columns if (col[:-2] == 'rainfall_' or col[-2:] == month)]
        #print('col_list: ',col_list)
        return col_list
    
    def save_df_to_csv(self, info):
        filename = '../../data/files/statistics/' + info + '_Correlacao.csv'
        with open(filename, 'w') as file:
            self.corr_dataset.to_csv(file)
    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.df = self.get_normalized_data()