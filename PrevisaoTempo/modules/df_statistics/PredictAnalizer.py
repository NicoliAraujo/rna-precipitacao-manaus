# -*- coding: utf-8 -*-
'''
Created on 31 de out de 2016

@author: pibic-elloa-nicoli
'''
import pandas as pd
import numpy as np
import scipy.stats as stats
import itertools
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from unittest.mock import inplace


class Predict_Best():
    def __init__(self, result_nets_csv, data_set_csv, num_nets, month):
        self.result_nets_df = self.read_data_set(result_nets_csv)
        
        
        self.data_set = self.read_data_set(data_set_csv)
        my_input = self.data_set.columns[1:]
        output = self.data_set.columns[0]


        self.train_data = {'input': self.data_set.loc[1950:2001][my_input], 
                           'output':self.data_set.loc[1950:2001][output]}
        #print(self.train_data)
        self.test_data = {'input': self.data_set.loc[2002:2015][my_input],
                          'output': self.data_set.loc[2002:2015][output]}
        
        self.start_predict_df(month)
        self.result_predict_list = []
        self.best_nets = self.start_nets(num_nets)
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(5)
    
    def start_predict_df(self, month):
        self.predict_df = pd.DataFrame(self.test_data['output'])
        self.predict_df.index = [i for i in range(len(self.test_data['output']))]
        self.predict_df.rename(columns = {'rainfall_'+str(month):'Anomaly'}, inplace = True)
        self.predict_df['Year'] = pd.Series(self.test_data['output'].index)
        self.predict_df['from'] = 'y'
    
    def start_nets(self, num_nets):
        best_nets=[]

        for i in range(1,num_nets+1):
            
            network = MLPRegressor(hidden_layer_sizes=eval(self.result_nets_df['Arquitetura'][i]),
                                   activation=self.result_nets_df['FA'][i], solver='sgd',
                                   alpha=self.result_nets_df['Alpha'][i],
                                   learning_rate_init=self.result_nets_df['TA'][i],
                                   verbose=False, early_stopping=True,
                                   validation_fraction=self.result_nets_df['FV'][i],
                                   max_iter=2000)
            best_nets.append(network)
            #print(network.hidden_layer_sizes, type(network.hidden_layer_sizes))
        return best_nets
    
    def train_predict(self):
        
        #print(self.train_data['input'], self.train_data['output'])
        for net in self.best_nets:
            net.fit(self.train_data['input'], self.train_data['output'])
            result_test_data = net.predict(self.test_data['input'])
            self.result_predict_list.append(result_test_data)
        #print(self.result_predict_list)
    
    def set_predict_df(self):
        i=1
        for net in self.result_predict_list:
            net = pd.DataFrame(net)
            net.rename(columns = {0:'Anomaly'}, inplace = True)
            net['Year'] = pd.Series(self.test_data['output'].index)
            net['from'] = 'net_'+str(i)
            #print(net)
            self.predict_df = self.predict_df.append(net, ignore_index=True)
            i+=1
        
        self.predict_df['Anomaly']*=100
        print(self.predict_df)
        
    def save_df(self, filename):
        with open(filename, 'w') as file:
            self.predict_df.to_csv(filename)
            
if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    RESULT_NETS_CSV = '../../data/files/ann_output_files/' + MONTH+ '_' + TIME_GAP + '_regression_dataset_normalized.csv'
    DATA_SET_CSV = '../../data/files/anninputs/normalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION

    PB = Predict_Best(RESULT_NETS_CSV, DATA_SET_CSV, 5, MONTH)
    PB.train_predict()
    PB.set_predict_df()
    FILENAME = '../../data/files/ann_output_files/predict_comp' + MONTH + '_' + TIME_GAP + '_regression_normalized.csv'
    PB.save_df(FILENAME)
