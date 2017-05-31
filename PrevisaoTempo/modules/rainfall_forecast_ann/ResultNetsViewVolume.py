# -*- coding: utf-8 -*-
'''
Created on 10 de mai de 2017

@author: pibic-elloa-nicoli
'''


import os

import pandas as pd


class ResultNetsView():
    '''Cria um dataset com a visualização da arquitetura, função de ativação, alpha, taxa de ativação, função de verificação, mse e nmse
    das redes neurais que foram treinadas
    '''
    def __init__(self, result_net_list):
        self.result_net_list = result_net_list
        self.df = pd.DataFrame()

    def set_df(self):
        '''fa = funçao de ativação
        ta = taxa de aprendizado
        fv= fração de validação
        '''
        
        dict_net = {'Arquitetura': [], 'FA': [], 'Alpha': [],
                'TA': [], 'FV': [],'ACURACIA': []}
        for result_net in self.result_net_list:
            dict_net['Arquitetura'].append(str(result_net.net.hidden_layer_sizes))
            dict_net['FA'].append(result_net.net.activation)
            dict_net['Alpha'].append(result_net.net.alpha)
            dict_net['TA'].append(result_net.net.learning_rate_init)
            dict_net['FV'].append(result_net.net.validation_fraction)
            #dict_net['MSE'].append(round(result_net.mse, 5))
            #dict_net['MAE'].append(round(result_net.mae, 5))
            dict_net['ACURACIA'].append(round(result_net.acuracia, 5))
        self.df = pd.DataFrame(dict_net)
        self.df.sort_values(by='ACURACIA', ascending=False,inplace=True)
        self.df.index = [i for i in range(1, len(self.df) + 1)]
        cols = ['Arquitetura', 'FA', 'Alpha', 'TA', 'FV', 'ACURACIA']
        self.df = self.df[cols]
        #print(self.df)
        #print(self.df.to_latex())
    def save_results(self, filename):
        os.makedirs(filename[0], exist_ok=True)
        name = filename[0]+filename[1]
        with open(name, 'w') as file:
            self.df.to_csv(name)
        with open(name[:-4]+'.tex', 'w') as file:
            file.write(self.df.to_latex())


class ResultsParser():
    '''classe que lê os resultados obtidos das redes e cria os seguintes dfs:
        -df com os resultados normalizados para o seaborn (parser_results_df_seaborn)
        -df com os resultados normalizados e em anomalia para o seaborn(parser_results_anomaly_df_seaborn)
        -df com os resultados normalizados (results_df)
        -df com os resultados em volume(results_df_volume)
        -df com os resultados normalizados e em anomalia (self.results_anomaly_df)
        -df com os resultados em volume e anomalia(results_anomaly_volume_df)
        -df com os resultados em anomalia do volume para o seaborn (self.parser_results_anomaly_volume_df_seaborn)
        -df com os resultados em volume para o seaborn(self.parser_results_df_volume_seaborn)        
        -df com os resultados em self. = pd.DataFrame()
        
        '''
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0)
    
    def __init__(self, result_nets_list, test_data, month, num_nets):
        self.result_nets_list = result_nets_list
        self.test_data = test_data
        self.month = month
        
        
        self.parser_results_anomaly_df_seaborn = pd.DataFrame()
        self.parser_results_df_seaborn = pd.DataFrame()       
        
        self.results_df = pd.DataFrame()
        self.results_anomaly_df = pd.DataFrame()
        
        self.num_nets = num_nets
        
        
    def set_parser_results_seaborn(self):
        '''parser do df dos resultados previstos x o encontrado pro seaborn'''
        self.parser_results_df_seaborn = pd.DataFrame(self.test_data['output'])
        self.parser_results_df_seaborn.index = [i for i in range(len(self.test_data['output']))]
        self.parser_results_df_seaborn.rename(columns={'rainfall_' + str(self.month):'Volume'}, inplace=True)
        self.parser_results_df_seaborn['Year'] = pd.Series(self.test_data['output'].index)
        self.parser_results_df_seaborn['from'] = 'y'
        for i in range(self.num_nets):
            results_predict = pd.DataFrame(self.result_nets_list[i].result_data_total)
            results_predict.rename(columns={0:'Volume'}, inplace=True)
            results_predict['Year'] = pd.Series(self.test_data['output'].index)
            results_predict['from'] = 'net_' + str(i)
            self.parser_results_df_seaborn = self.parser_results_df_seaborn.append(results_predict)
        self.parser_results_df_seaborn.index = [i for i in range(1, len(self.parser_results_df_seaborn)+1)]
        print('\nresultsdfseaborn',self.parser_results_df_seaborn)
    def set_seaborn_dfs(self):
        '''datasets para seaborn'''
        self.set_parser_results_seaborn()
        self.parser_results_anomaly_df_seaborn = self.from_abs_to_anomaly(self.parser_results_df_seaborn, 'Volume')
        print('\nresults anomalia pro seaborn', self.parser_results_anomaly_df_seaborn)

    def save_df(self, filename, df):
        os.makedirs(filename[0], exist_ok=True)
        with open(filename[0] + filename[1], 'w') as file:
            df.to_csv(filename[0] + filename[1])
    
    def set_results_dfs(self):
        '''Datasets para visualização'''
        self.results_df['y'] = self.test_data['output']
        for i in range(self.num_nets):
            self.results_df['net_' + str(i)] = self.result_nets_list[i].result_data_total
            self.results_df.index = self.test_data['output'].index
        #print('resultsdf',self.results_df)
        self.results_anomaly_df = self.from_abs_to_anomaly(self.results_df)
        #print('results anomalia', self.results_anomaly_df)

    def from_abs_to_anomaly(self, df, attr=None):
        if attr == None:
            attr = df.columns
        anomaly_df = df.copy()
        anomaly_df[attr] -= self.results_df['y'].mean()
        return anomaly_df

    
    def save_results_dfs(self, filename_norm_results_view, filename_norm_results_anomaly_view):
        self.save_df(filename_norm_results_view, self.results_df)
        self.save_df(filename_norm_results_anomaly_view, self.results_anomaly_df)

        
    def save_seaborn_dfs(self, filename_results_norm_seaborn, filename_norm_anomaly_seaborn):
        self.save_df(filename_results_norm_seaborn, self.parser_results_df_seaborn)
        self.save_df(filename_norm_anomaly_seaborn, self.parser_results_anomaly_df_seaborn)
