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
        return "{0}: \nMSE treinamento: {1}\nMSE teste: {2}\nMAPE teste: {3}%\n".format(self.net, self.mse_test, self.mse_test, self.mape_test)
    
    def __lt__(self, other):
        if self.mape_test < other.mape_test:
            return True
        else:
            return False
        
class RainfallRegressor(object):
    '''
    Treinar, testar e validar um conjunto de dados de 1950 a 2015 com as anomalias
    dos dados mensais de precipitação, tsa, e ninos. O output deve ser o volume de
    cada mês, e o input são os dados de uma quantidade time_gap de meses antes do
    mês avaliado.

    1) ler dataset
    2) identificar inputs
    3) identificar output
    4) setar rede:
        tipo: time series
        medida de performance: mse
        passar input
        passar output

        net.trainParam.epochs = 100;
        net.trainParam.mu = 0.003;
        net.trainParam.mu_dec = 0.01;
        net.trainParam.mu_inc = 7;
        net.trainParam.mu_max = 10^10;


    5)dividir:
        função de treinamento: divideblock
        quantidades de dados que irão para treinamento, validação e teste
    6) setar parâmetros de treinamentos:

    7)qtdLayers = 10;
    netLayers = (1:qtdLayers);

    mseVCT = zeros(qtdLayers:1);
    mapeVCT = zeros(qtdLayers:1);

    for i = 1:qtdLayers
        clear train;
        net.layers{1}.dimensions = netLayers(i);
        net = configure(net,trainData,target);
        [net,tr] = train(net, trainData, target);

        %getting performance parameters
        %getting Mean Square Error
        result = net(trainData);
        error = result - target;
        mseVCT(i,1) = mse(error);

        %getting Mean Absolute Percentage Error (MAPE)
        [nRowsTD,nCollumnsTD] = size(tr.testInd);
        errorTestData = zeros(2,nRowsTD);
        for j = 1:nRowsTD
            indice = tr.testInd(:,j);
            errorTestData(:,j) = result(:,indice) - target(:,indice);
        end
        mapeVCT(i,1) = 100*(mae(errorTestData));
    end


    %display perform parameters
    display(mapeVCT);
    %display((100 - mapeVCT))
    display(mseVCT);

    '''

    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(5)

    def set_layers(self, n_layers, n_nodes):
        '''mudar implementação pra ter layers em função de nlayers
        '''
        layers = []
        nodelist = [i for i in range(1,n_nodes+1)]
        layers.append(itertools.product(nodelist, nodelist, repeat=1))
        layers.append(itertools.product(nodelist, repeat=1))
        '''for i in layers:
            for j in i:
                print(j)'''
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
                                                       activation=act, solver='sgd',
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
        filename = '../../data/files/ann_output_files/' + month+ '_' + time_gap + '_regression_dataset_normalized' + etc + '.txt'
        self.result_networks = sorted(self.result_networks, key= lambda ResultNet: ResultNet.mape_test)

        with open(filename, 'w') as file:
            for result_network in self.result_networks:
                file.write(str(result_network))

    def fit_networks(self):
        for network in self.neural_networks:
            network = network.fit(self.train_data['input'], self.train_data['output'])
            #print(network.score(self.test_data[0], self.test_data[1]))

            #print(network.loss_)

if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    FILENAME = '../../data/files/anninputs/normalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    RFANN = RainfallRegressor(FILENAME, n_layers=2, n_nodes=7)
    RFANN.fit_networks()
    RFANN.predict_networks()
    RFANN.save_networks(MONTH, TIME_GAP)
    