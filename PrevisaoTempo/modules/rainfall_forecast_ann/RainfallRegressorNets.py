# -*- coding: utf-8 -*-
'''
Created on 27 de abr de 2017

@author: pibic-elloa-nicoli
'''
import itertools
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.neural_network.multilayer_perceptron import MLPRegressor

from modules.rainfal_forecast_ann.Regressor import ResultDataSet, ResultNet
import pandas as pd
import scipy.stats as stats


class RainfallRegressorNets(object):
    '''
    Instancia, treina e testa todas as redes neurais
    '''

    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0)

    def set_layers(self, n_layers, n_nodes):
        '''mudar implementação pra ter layers em função de nlayers
        '''
        layers = []
        nodelist = [i for i in range(1,n_nodes+1)]
        layers.append(itertools.product(nodelist, nodelist, repeat=1))
        layers.append(itertools.product(nodelist, repeat=1))
        return layers
    def start_networks(self, n_layers, n_nodes):
        '''inicializa as redes a ser testadas'''
        neural_networks = []
        hidden_layers = self.set_layers(n_layers, n_nodes)
        for layer_setup in hidden_layers:
            for node_setup in layer_setup:
                for act in ['logistic', 'tanh']:
                    for my_alpha in [0.0001, 0.01]:
                        for my_learning_rate_init in [0.001,0.003]:
                            for my_validation_fraction in [0.1,0.0462]:
                                network = MLPRegressor(hidden_layer_sizes=node_setup,
                                                       activation=act, solver='lbfgs',
                                                       alpha=my_alpha,
                                                       learning_rate_init=my_learning_rate_init,
                                                       verbose=False, early_stopping=True,
                                                       validation_fraction=my_validation_fraction,
                                                       max_iter=2000)
                                neural_networks.append(network)
        return neural_networks

    def __init__(self, filename, n_layers, n_nodes):
        '''
        Constructor
        '''
        self.data_set = self.read_data_set(filename)
        #print(self.data_set.dtypes)
        my_input = self.data_set.columns[1:]
        output = self.data_set.columns[0]

        #print(self.data_set.corr())
        #print(my_input, output)

        self.train_data = {'input': self.data_set.loc[1950:2000][my_input],
                           'output':self.data_set.loc[1950:2000][output]}

        self.test_data = {'input': self.data_set.loc[2001:2015][my_input],
                          'output': self.data_set.loc[2001:2015][output]}
        #print(self.test_data)
        self.neural_networks = self.start_networks(n_layers, n_nodes)
        self.result_networks = []
        print(self.train_data, self.test_data)

    def predict_networks(self):
        '''não retorna valores corretos'''
        for network in self.neural_networks:

            result_train_data = network.predict(self.train_data['input'])
            result_test_data = network.predict(self.test_data['input'])

            result_net = ResultNet(network,
                                   (self.train_data['output'], result_train_data),
                                   (self.test_data['output'], result_test_data))
            self.result_networks.append(result_net)
            #print(result_net)

    def save_networks(self, month, time_gap, etc=''):
        filename = '../../data/files/ann_output_files/' + month+ '_' + time_gap + '_regression_dataset_normalized' + etc + '.csv'
        result_data_set = ResultDataSet(self.result_networks)
        result_data_set.set_df()
        result_data_set.save_results(filename)
        print(result_data_set.df)

    def fit_networks(self):
        i=0
        for network in self.neural_networks:

            network = network.fit(self.train_data['input'], self.train_data['output'])
            #print(network.score(self.test_data['input'], self.test_data['output']))
            print(i)
            i+=1
        print(self.neural_networks)
            #print(network.loss_)
