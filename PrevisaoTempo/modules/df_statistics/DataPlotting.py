# -*- coding: utf-8 -*-
'''
Created on 13 de out de 2016

@author: pibic-elloa-nicoli
'''
import seaborn as sns
from pandas.tseries.index import DatetimeIndex

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class DataPlotting(object):
    '''
    classdocs
    '''
    def get_data_frame(self, path):
        return pd.read_csv(path, sep=r',', index_col='Year')
    
    def get_param_mean(self, param):
        return self.month_data_frame[param].mean()
    
    def get_month_data(self, param):
        month_data_frame = pd.DataFrame()
        for name in self.data_frame.columns:
            if name[-2:] == self.month:
                month_data_frame[name[:-3]] = self.data_frame[name]
        month_data_frame.index = self.data_frame.index
        month_data_frame.index.name = self.data_frame.index.name
        return month_data_frame

    def set_graph(self, param, param_name):
        month_data_frame = self.get_month_data(param)
        # print(month_data_frame)
        plt.clf()
        plt.figure(figsize=(30, 15))
        bar_graph = sns.barplot(x=month_data_frame.index, y=param, data=month_data_frame, color="#808080")
        # plt.setp(bar_graph.get_xticklabels(), rotation=45)
        bar_graph.set(xlabel=month_data_frame.index.name, ylabel=param_name)
        sns.plt.savefig('../../data/images/anomalydata/' + self.month + param + '.pdf')
        sns.plt.savefig('../../data/images/anomalydata/' + self.month + param + '.png')
        plt.close()
    
    def __init__(self, month, path):
        self.month = month
        self.data_frame = self.get_data_frame(path)

    
if __name__ == '__main__':
    PATH = '../../data/files/anomalydata/AllAnomalyData.csv'
    PLT = DataPlotting('01', PATH)
    PLT.set_graph('rainfall', 'Rainfall')
    PLT.set_graph('tsa', 'TSA')
    PLT.set_graph('nino3', 'Nino 3')
    PLT.set_graph('nino4', 'Nino 4')
    PLT.set_graph('nino34', 'Nino 3.4')
    PLT.set_graph('nino12', 'Nino 1+2')
