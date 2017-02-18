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
                'TA': [], 'FV': [], 'MAPE Teste': [], 'Acurácia': []}
        for result_net in self.result_net_list:
            #print(result_net.net.hidden_layer_sizes)
            dict_net['Arquitetura'].append(str(result_net.net.hidden_layer_sizes))
            dict_net['FA'].append(result_net.net.activation)
            dict_net['Alpha'].append(result_net.net.alpha)
            dict_net['TA'].append(result_net.net.learning_rate_init)
            dict_net['FV'].append(result_net.net.validation_fraction)
            #dict_net['MSE Treinamento'].append(round(result_net.mse_train,5))
            #dict_net['MSE Teste'].append(round(result_net.mse_test,5))
            dict_net['MAPE Teste'].append(round(result_net.mape_test, 3))
            dict_net['Acurácia'].append(round(100-result_net.mape_test, 3))
        self.df = pd.DataFrame(dict_net)
        #print(self.df)
        self.df.sort_values(by='MAPE Teste', ascending=True, inplace=True)
        self.df.index = [i for i in range(1, len(self.df)+1)]
        #cols = ['Arquitetura', 'FA', 'Alpha', 'TA', 'FV', 'MSE Treinamento', 
        #        'MSE Teste', 'MAPE Teste',  'Acurácia']
        cols = ['Arquitetura', 'FA', 'Alpha', 'TA', 'FV', 'MAPE Teste',  'Acurácia']
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
        self.__mape_test = 100*mae(test_expected, test_obtained)

    def __repr__(self):
        return "{0}: \nMSE treinamento: {1}\nMSE teste: {2}\nMAPE teste: {3}%\n\n".format(self.net, self.mse_test, self.mse_test, self.mape_test)
    
    def __lt__(self, other):
        if self.mape_test < other.mape_test:
            return True
        else:
            return False
        
class RainfallRegressor(object):
    '''
    
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
                                                       max_iter=200000)
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
        #print(input, output)

        self.train_data = {'input': self.data_set.loc[1950:2001][my_input], 
                           'output':self.data_set.loc[1950:2001][output]}
        
        self.test_data = {'input': self.data_set.loc[2002:2015][my_input], 
                          'output': self.data_set.loc[2002:2015][output]}
        #print(self.test_data)
        self.neural_networks = self.start_networks(n_layers, n_nodes)
        self.result_networks = []
        #print(self.train_data, self.test_data)

    def predict_networks(self):
        '''não retorna valores corretos'''
        for network in self.neural_networks:

            result_train_data = network.predict(self.train_data['input'])
            result_test_data = network.predict(self.test_data['input'])

            result_net = ResultNet(network, 
                                   (self.train_data['output'], result_train_data),
                                   (self.test_data['output'], result_test_data))
            self.result_networks.append(result_net)

    def save_networks(self, month, time_gap, etc=''):
        filename = '../../data/files/ann_output_files/' + month+ '_' + time_gap + '_regression_dataset_normalized' + etc + '.csv'
        result_data_set = ResultDataSet(self.result_networks)
        result_data_set.set_df()
        result_data_set.save_results(filename)
       

    def fit_networks(self):
        for network in self.neural_networks:
            network = network.fit(self.train_data['input'], self.train_data['output'])
            #print(network.score(self.test_data[0], self.test_data[1]))

            #print(network.loss_)

class Predict_Best():
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0)
    
    def __init__(self, result_nets_list, test_data, month, num_nets):
        self.result_nets_list = result_nets_list
        self.test_data = test_data
        self.month = month
        self.predict_df = pd.DataFrame()
        
        self.num_nets = num_nets
        self.start_predict_df_seaborn()
        
    def start_predict_df_seaborn(self):
        self.predict_df_seaborn = pd.DataFrame(self.test_data['output'])
        self.predict_df_seaborn.index = [i for i in range(len(self.test_data['output']))]
        self.predict_df_seaborn.rename(columns = {'rainfall_'+str(self.month):'Norm'}, inplace = True)
        self.predict_df_seaborn['Year'] = pd.Series(self.test_data['output'].index)
        self.predict_df_seaborn['from'] = 'y'
        
    def set_predict_df(self):
        
        self.predict_df['y'] = self.test_data['output']
        for i in range(self.num_nets):
            self.predict_df['net_'+ str(i)] = self.result_nets_list[i].net.predict(self.test_data['input'])
            self.predict_df.index = self.test_data['output'].index
        #print(self.predict_df)
 
    def set_predict_df_seaborn(self):
        for i in range(self.num_nets):
            results_predict = pd.DataFrame(self.result_nets_list[i].net.predict(self.test_data['input']))
            results_predict.rename(columns = {0:'Norm'}, inplace = True)
            results_predict['Year'] = pd.Series(self.test_data['output'].index)
            results_predict['from'] = 'net_'+str(i)
            self.predict_df_seaborn = self.predict_df_seaborn.append(results_predict)
        #print(self.predict_df_seaborn)
        
    def save_predict_df(self, filename):
        with open(filename, 'w') as file:
            self.predict_df_seaborn.to_csv(filename)
            
    def save_predict_df_seaborn(self, filename):
        with open(filename, 'w') as file:
            self.predict_df_seaborn.to_csv(filename)

    def start_predict_dfs_volume(self, filename):
        self.source_df_sum = self.read_data_set(filename).sum()
        
        self.predict_df = self.predict_df*self.source_df_sum['rainfall_'+self.month]
        self.predict_df_seaborn['Norm'] = self.predict_df_seaborn['Norm']*self.source_df_sum['rainfall_'+self.month]
        
    def save_predict_df_volume(self, filename_seaborn, filename):
        with open(filename_seaborn, 'w') as file:

            self.predict_df_seaborn.to_csv(filename_seaborn)
        with open(filename, 'w') as file:
            
            self.predict_df.to_csv(filename)
    
        
if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    FILENAME = '../../data/files/anninputs/normalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    RFANN = RainfallRegressor(FILENAME, n_layers=2, n_nodes=7)
    RFANN.fit_networks()
    RFANN.predict_networks()
    RFANN.save_networks(MONTH, TIME_GAP)
    
    RESULT_NETS_CSV = '../../data/files/ann_output_files/' + MONTH+ '_' + TIME_GAP + '_regression_dataset_normalized.csv'
    
    PB = Predict_Best(RFANN.result_networks, RFANN.test_data, MONTH, num_nets=5)
    PB.set_predict_df()
    PB.set_predict_df_seaborn()
    FILENAME_PREDICT = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_normalized.csv'
    FILENAME_PREDICT_SEABORN = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_normalized_seaborn.csv'
    PB.save_predict_df_seaborn(FILENAME_PREDICT_SEABORN)
    PB.save_predict_df(FILENAME_PREDICT)
    
    FILENAME_SOMA_SEABORN = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_volume_seaborn.csv'
    FILENAME_SOMA = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_volume.csv'
    
    FILENAME_SOURCE_SOMA = '../../data/files/original/AllData.csv'
    
    
    PB.start_predict_dfs_volume(FILENAME_SOURCE_SOMA)
    PB.save_predict_df_volume(FILENAME_SOMA_SEABORN, FILENAME_SOMA)
