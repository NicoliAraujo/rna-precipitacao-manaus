# -*- coding: utf-8 -*-
'''
Created on 27 de abr de 2017

@author: pibic-elloa-nicoli
'''

from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale

from ResultNetsViewVolume import ResultNetsView, ResultsParser
import numpy as np
import pandas as pd


class RainfallRegressorNets(object):
    '''
    Instancia, treina e testa todas as redes neurais
    '''

    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0)

    def start_networks(self):
        '''inicializa as redes a ser testadas'''
        neural_networks = []
        # hidden_layers = self.set_layers(n_layers, n_nodes)
        hidden_layers = [(3, 9), (4, 8), (5, 7), (6, 6), (7, 5), (8, 4), (9, 3),
                          (3), (4), (5), (6), (7), (8), (9), (10), (11), (12)]
        for layer_setup in hidden_layers:
            for act in ['logistic', 'tanh']:
                for my_alpha in [0.0001, 0.01]:
                    for my_learning_rate_init in [0.001, 0.003]:
                        for my_validation_fraction in [0.1, 0.2]:
                            network = MLPRegressor(hidden_layer_sizes=layer_setup,
                                                   activation=act, solver='sgd',
                                                   alpha=my_alpha,
                                                   learning_rate_init=my_learning_rate_init,
                                                   verbose=False, early_stopping=True,
                                                   validation_fraction=my_validation_fraction,
                                                   max_iter=2000)
                            neural_networks.append(RainfallNet(network, self.train_data, self.test_data))
        return neural_networks
        '''hidden_layers = [(3, 9), (4, 8), (10), (11), (12)]
        for layer_setup in hidden_layers:
            for act in ['logistic', 'tanh']:
                for my_alpha in [0.0001, 0.01]:
                    for my_learning_rate_init in [0.001]:
                        for my_validation_fraction in [0.1]:
                            network = MLPRegressor(hidden_layer_sizes=layer_setup,
                                                   activation=act, solver='sgd',
                                                   alpha=my_alpha,
                                                   learning_rate_init=my_learning_rate_init,
                                                   verbose=False, early_stopping=True,
                                                   validation_fraction=my_validation_fraction,
                                                   max_iter=200)
                            neural_networks.append(RainfallNet(network, self.train_data, self.test_data))
        return neural_networks'''

    def __init__(self, dataset_non_normalized):
        '''
        Constructor
        '''
        self.train_data, self.test_data = self.set_train_test_data(dataset_non_normalized)
        
        self.neural_networks = self.start_networks()
    
    def set_train_test_data(self, dataset):
        data_set = dataset
        my_input = data_set.columns[1:]
        output = data_set.columns[0]
        self.train_data, self.test_data = self.set_train_test_data(dataset_non_normalized)
        self.neural_networks = self.start_networks()
    
    def set_train_test_data(self, dataset):
        data_set = dataset
        my_input = data_set.columns[1:]
        output = data_set.columns[0]

        train_data = {'input': data_set.loc[1950:2000][my_input],
                           'output':data_set.loc[1950:2000][output]}

        test_data = {'input': data_set.loc[2001:2015][my_input],
                          'output': data_set.loc[2001:2015][output]}
        

        return train_data, test_data
    def train_test_nets(self):
        '''método que treina e obtem o mae e o mse para cada rede treinada 100x'''
        i=0
        #print(len(self.neural_networks))
        for net in self.neural_networks:
            #print(i)
            net.train_test()
            i+=1

    def save_networks(self, month, time_gap, etc=''):
        filename = ['../../data/files/ann_output_files/scale/', month + '_' + time_gap + '_scale' + etc + '.csv']
        result_data_set = ResultNetsView(self.neural_networks)
        result_data_set.set_df()
        result_data_set.save_results(filename)
        #print(result_data_set.df)

class RainfallNet():
    '''
    Cria um objeto de cada rede neural treinada e testada
    '''
    def __init__(self, net, train_data, test_data):
        self.net = net
        self.media = pd.concat([train_data['output'], test_data['output']]).mean()
        #print(pd.concat([train_data['output'], test_data['output']]))
        
        self.std_scaler = StandardScaler()
        #print(train_data['input'].shape)
        self.train_data = {'input': scale(train_data['input']),
                           'output': scale(train_data['output'])}
        
        self.test_data = {'input': scale(test_data['input']),
                           'output': test_data['output']}
        self.std_scaler.fit_transform(test_data['output'].values.reshape(-1,1))
        self.result_data_total=np.zeros(len(self.test_data['output']))
        self.mae = 0
        self.mse = 0
        self.acuracia=0
        
    def set_dif(self, df):
        df = df-self.media
        df.loc[df<0] = int(0)
        df.loc[df>0] = 1
        return df
    
    def myacuracia(self):
        dif_test_data = pd.DataFrame({'result': self.set_dif(self.test_data['output'])})
        
        self.result_data_total = pd.Series(self.result_data_total, index=dif_test_data.index)
        #print(self.result_data_total)
        dif_predicted = pd.DataFrame({'result': self.set_dif(self.result_data_total)})
        
        dif = dif_test_data - dif_predicted
        #print(dif)
        result = dif.loc[dif['result']==0].size
        self.acuracia = max(result/len(dif),self.acuracia)
        
    def train_test(self):   
        
        for i in range(10):
            #print('it: ', i)
            #print(self.train_data['input'].shape, self.train_data['output'].shape)
            self.net = self.net.fit(self.train_data['input'], self.train_data['output'].ravel())
            #result_test_data = self.net.predict(self.test_data['input'])
            result_test_data = self.std_scaler.inverse_transform(self.net.predict(self.test_data['input']))
            self.result_data_total=result_test_data
            #print(result_test_data, self.test_data['output'])
            self.mae += mae(self.test_data['output'], result_test_data)
            self.mse += mse(self.test_data['output'], result_test_data)
            self.myacuracia()
            #print(self.mae, self.mse)
        self.mse /= 10
        self.mae /= 10
        print(self.acuracia)
        #print(self.result_data_total)
        #print(self.mae, self.mse)

    def __repr__(self):
        return "{0}: \nMSE: {1}\nMAE: {2}%\n\n".format(self.net, self.mse, self.mae)

    def __lt__(self, other):
        if self.mse < other.mse:
            return True
        else:
            return False

