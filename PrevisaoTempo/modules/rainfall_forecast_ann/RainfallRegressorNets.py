# -*- coding: utf-8 -*-
'''
Created on 27 de abr de 2017

@author: pibic-elloa-nicoli
'''
import itertools
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.neural_network.multilayer_perceptron import MLPRegressor

from modules.rainfall_forecast_ann.ResultNetsView import ResultNetsView 
import pandas as pd


class RainfallRegressorNets(object):
    '''
    Instancia, treina e testa todas as redes neurais
    '''

    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0)

    def start_networks(self, n_layers, n_nodes):
        '''inicializa as redes a ser testadas'''
        neural_networks = []
        #hidden_layers = self.set_layers(n_layers, n_nodes)
        hidden_layers = [(3,9), (4,8), (5,7), (6,6), (7,5), (8,4), (9,3),
                          (3), (4), (5), (6), (7), (8), (9), (10), (11), (12)]
        for layer_setup in hidden_layers:
            for act in ['logistic', 'tanh']:
                for my_alpha in [0.0001, 0.01]:
                    for my_learning_rate_init in [0.001,0.003]:
                        for my_validation_fraction in [0.1,0.2]:
                            network = MLPRegressor(hidden_layer_sizes=layer_setup,
                                                   activation=act, solver='lbfgs',
                                                   alpha=my_alpha,
                                                   learning_rate_init=my_learning_rate_init,
                                                   verbose=False, early_stopping=True,
                                                   validation_fraction=my_validation_fraction,
                                                   max_iter=2000)
                            neural_networks.append(RainfallNet(network, self.train_data, self.test_data))
        return neural_networks

    def __init__(self, filename, n_layers, n_nodes):
        '''
        Constructor
        '''
        self.data_set = self.read_data_set(filename)
        my_input = self.data_set.columns[1:]
        output = self.data_set.columns[0]

        self.train_data = {'input': self.data_set.loc[1950:2000][my_input],
                           'output':self.data_set.loc[1950:2000][output]}

        self.test_data = {'input': self.data_set.loc[2001:2015][my_input],
                          'output': self.data_set.loc[2001:2015][output]}
        self.neural_networks = self.start_networks(n_layers, n_nodes)
        print(len(self.neural_networks))
        print(self.train_data, self.test_data)
        
    def train_test_nets(self):
        '''método que treina e obtem o mae e o mse para cada rede treinada 100x'''
        for net in self.neural_networks:
            net.train_test()

    def save_networks(self, month, time_gap, etc=''):
        filename = '../../data/files/ann_output_files/' + month+ '_' + time_gap + '_regression_dataset_normalized' + etc + '.csv'
        result_data_set = ResultNetsView(self.neural_networks)
        result_data_set.set_df()
        result_data_set.save_results(filename)
        print(result_data_set.df)

class RainfallNet():
    '''
    Cria um objeto de cada rede neural treinada e testada
    '''
    def __init__(self, net, train_data, test_data):
        self.net = net
        self.train_data = train_data
        self.test_data = test_data
        self.mae = 0
        self.mse = 0
    
    def train_test(self):    
        for i in range(100):
            self.net = self.net.fit(self.train_data['input'], self.train_data['output'])
            result_test_data = self.net.predict(self.test_data['input'])
            self.mae+=mae(self.test_data['output'], result_test_data)
            self.mse+=mse(self.test_data['output'], result_test_data)
        self.mse/=100
        self.mae/=100
    
    def __repr__(self):
        return "{0}: \nMSE: {1}\nMAE: {2}%\n\n".format(self.net, self.mse, self.mae)

    def __lt__(self, other):
        if self.mse < other.mse:
            return True
        else:
            return False


