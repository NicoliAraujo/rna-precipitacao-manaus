'''
Created on 6 de mar de 2017

@author: pibic-elloa-nicoli
'''
import pandas as pd


class Normalizador(object):
    '''
    classdocs
    '''
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(10)

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.dataframe = self.read_data_set(filename)
        
    def normalize_data(self):
        df = self.dataframe
        
        for name in self.dataframe.columns:
            df[name] = self.dataframe[name] / self.dataframe[name].abs().sum()
            self.dataframe = df
        print(self.dataframe)
    
    def save(self):
        filename = '../../data/files/original/AllNormalizedData.csv'
        with open(filename, 'w') as file:
            self.dataframe.to_csv(file, sep=r',')
            
             
if __name__ == '__main__':
    PATH_INPUT = '../../data/files/original/AllData.csv'
    norm = Normalizador(PATH_INPUT)
    norm.normalize_data()
    norm.save()
    
