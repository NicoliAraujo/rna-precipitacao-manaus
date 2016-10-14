'''
Created on 26 de set de 2016

@author: pibic-elloa-nicoli
'''
import pandas as pd


class Anomaly(object):
    '''
    classdocs
    '''
    def get_original_data(self):
        filepath = '../data/original/csv/' + self.name + '.csv'
        return pd.read_csv(filepath, sep = r',', index_col = 'Year')

    def set_anomaly_df(self):
        self.anomaly_df = self.df - self.df.mean()

    def save_df_to_csv(self):
        filename = '../data/files/anomalydata/' + self.name + '.csv'
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
