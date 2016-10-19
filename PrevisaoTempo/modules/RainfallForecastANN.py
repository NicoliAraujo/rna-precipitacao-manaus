# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2016

@author: Nicoli
'''
import pandas as pd
import sklearn

class RainfallForecastANN(object):
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
    6) setar parâmetros de treinamentos:7)qtdLayers = 10;
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
        return pd.read_csv(filename, sep=r',', index_col=0)
    
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.data_set = self.read_data_set(filename)
        #print(self.data_set)
        #print(self.data_set.dtypes)
        self.train_data = self.data_set.loc[1950:2001]
        self.val_data = self.data_set.loc[2002:2004]
        self.test_data = self.data_set.loc[2005:2015]
        #print(self.train_data, self.val_data, self.test_data)
        
if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    FILENAME = '../data/files/anninputs/anomalyinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    RFANN = RainfallForecastANN(FILENAME)
        