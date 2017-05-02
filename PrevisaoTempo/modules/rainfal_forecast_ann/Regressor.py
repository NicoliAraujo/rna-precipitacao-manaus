# -*- coding: utf-8 -*-
'''
Created on 31 de out de 2016

@author: pibic-elloa-nicoli
'''
import pandas as pd
import scipy.stats as stats
import itertools
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae


class ResultDataSet():
    def __init__(self, result_net_list):
        self.result_net_list = result_net_list
        self.df = pd.DataFrame()

    def set_df(self):
        '''fa = funçao de ativação
        ta = taxa de aprendizado
        fv= fração de validação
        '''
        #dict_net = {'Arquitetura': [], 'FA': [], 'Alpha': [],
        #        'TA': [], 'FV': [], 'MSE Treinamento': [],
        #        'MSE Teste': [], 'MAPE Teste': [], 'Acurácia': []}
        dict_net = {'Arquitetura': [], 'FA': [], 'Alpha': [],
                'TA': [], 'FV': [], 'MSE': [], 'NMSE':[]}
        for result_net in self.result_net_list:
            #print(result_net.net.hidden_layer_sizes)
            dict_net['Arquitetura'].append(str(result_net.net.hidden_layer_sizes))
            dict_net['FA'].append(result_net.net.activation)
            dict_net['Alpha'].append(result_net.net.alpha)
            dict_net['TA'].append(result_net.net.learning_rate_init)
            dict_net['FV'].append(result_net.net.validation_fraction)
            #dict_net['MSE Treinamento'].append(round(result_net.mse_train,5))
            dict_net['MSE'].append(round(result_net.mse_test,5))
            #dict_net['MAPE Teste'].append(round(result_net.mape_test, 3))
            #dict_net['Acurácia'].append(round(100-result_net.mape_test, 3))
        self.df = pd.DataFrame(dict_net)
        #print(self.df)
        self.df.sort_values(by='MSE', ascending=True, inplace=True)
        self.df.index = [i for i in range(1, len(self.df)+1)]
        #cols = ['Arquitetura', 'FA', 'Alpha', 'TA', 'FV', 'MSE Treinamento',
        #        'MSE Teste', 'MAPE Teste',  'Acurácia']
        cols = ['Arquitetura', 'FA', 'Alpha', 'TA', 'FV', 'MSE', 'NMSE']
        self.df = self.df[cols]
        #print(self.df)

    def save_results(self, filename):
        with open(filename, 'w') as file:
            self.df.to_csv(filename)

class ResultNet():
    def __init__(self, net, train_data, test_data):
        self.net = net
        self.mse_train = train_data
        self.mse_test = test_data
        self.mape_test = test_data

    @property
    def net(self):
        return self.__net

    @net.setter
    def net(self, net):
        if hasattr(net, 'coefs_') == True:
            self.__net = net
        else:
            print("A rede ainda não foi treinada!")

    @property
    def mse_train(self):
        return self.__mse_train

    @mse_train.setter
    def mse_train(self, train_data) :
        train_expected, train_obtained = train_data
        self.__mse_train = mse(train_expected, train_obtained)

    @property
    def mse_test(self):
        return self.__mse_test

    @mse_test.setter
    def mse_test(self, test_data):
        test_expected, test_obtained = test_data
        self.__mse_test = mse(test_expected, test_obtained)

    @property
    def mape_test(self):
        return self.__mape_test

    @mape_test.setter
    def mape_test(self, test_data):
        test_expected, test_obtained = test_data
        dif = abs(test_expected - abs(test_obtained))/test_expected
        self.__mape_test = 100/len(dif) * dif.sum()

    def __repr__(self):
        return "{0}: \nMSE treinamento: {1}\nMSE teste: {2}\nMAPE teste: {3}%\n\n".format(self.net, self.mse_test, self.mse_test, self.mape_test)

    def __lt__(self, other):
        if self.mape_test < other.mape_test:
            return True
        else:
            return False

