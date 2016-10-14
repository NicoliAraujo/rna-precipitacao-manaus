# -*- coding: utf-8 -*-
'''
Created on 26 de set de 2016
@author: pibic-elloa-nicoli
'''
from FromTxtToCSV import MMFromTxtToCSV
from DataStatistics import Anomaly
import pandas as pd
from itertools import cycle

class JoinDataFrame():
    '''colocar toda a parte de juntar os dataframes aqui:
    1) chamar original do .txt
    2) chamar anomalies
    3) editar limites de anos
    4) colocar tudo num df só
    5) salvar
    '''

    def set_original(self, path, sep_list, name):
        ''' '''
        parser_txt_csv = MMFromTxtToCSV(path)
        parser_txt_csv.set_csv(sep_list, name)
        parser_txt_csv.save_csv(name)
        return parser_txt_csv.data_frame

    def set_anomalies(self, name):
        ''' '''
        parser_anomaly = Anomaly(name)
        parser_anomaly.set_anomaly_df()
        return parser_anomaly.anomaly_df

    def set_years(self, data_frame, lim1, lim2):
        data_frame = data_frame[data_frame.index >= lim1]
        data_frame = data_frame[data_frame.index <= lim2]
        return data_frame

    def set_df_col_name(self, df_dict, name):
        namelist = []
        #print(self.dfDict[name])
        for collumn in df_dict[name]:
            namelist.append(collumn)
            #print(namelist, collumn)
        for i in range(len(namelist)):
            #print(collumn)
            namelist[i] = name + '_' + namelist[i]
        #print(namelist)
        df_dict[name].columns = namelist
        return df_dict

    def join(self):
        '''concatena os dataframes desejados'''
        for name in self.data_sequence_list:
            self.join_df = pd.concat([self.join_df, self.df_dict[name]], axis=1)
        #print(self.Joindf)

    def set_join_dict(self, data_dict):
        '''formata um dicionário de dataframes com os dados inputados no main'''
        for key in self.data_dict:
            #print(key)
            df_dict = {}
            path = data_dict[key][0]
            sep = data_dict[key][1]
            name = data_dict[key][2]
            #print(path, sep, name)
            #1) pegar os original
            data_frame = self.set_original(path, sep, name)
            #)setar anomalias
            data_frame = self.set_anomalies(name)
            #3)setar anos
            data_frame = self.set_years(data_frame, 1950, 2015)

            df_dict[name] = data_frame
            #setar colunas
            df_dict = self.set_df_col_name(df_dict, name)
        return df_dict
        #print(self.dfDict)
    def save_join(self):
        '''salva o df gerado em um csv'''
        with open('../data/files/anomalydata/AllAnomalyData.csv', 'w') as file:
            self.join_df.to_csv(file)

    def __init__(self, data_dict, data_sequence_list):
        self.data_dict = data_dict
        self.data_sequence_list = data_sequence_list
        self.df_dict = self.set_join_dict(self.data_dict)
        #print(self.dfDict[])
        #print(self.dfDict['rainfall'].columns)
        #print(self.dfDict['rainfall'])
        self.join_df = pd.DataFrame()
        #self.join(self.dfDict)

if __name__ == '__main__':
    DATA_DICT = {'rainfall': ['../data/original/other/rainfall.txt', ['\t'], 'rainfall'],
                 'nino12': ['../data/original/other/nino1+2.txt', ['  '], 'nino12'],
                 'nino3': ['../data/original/other/nino3.txt', ['  '], 'nino3'],
                 'nino34':['../data/original/other/nino34.txt', ['  '], 'nino34'],
                 'nino4': ['../data/original/other/nino4.txt', ['  '], 'nino4'],
                 'tsa':['../data/original/other/tsa.txt', ['    ', '   '], 'tsa']}
    DATA_SEQUENCE_LIST = [name for name in DATA_DICT]
    JOIN = JoinDataFrame(DATA_DICT, DATA_SEQUENCE_LIST)
    JOIN.join()
    JOIN.save_join()
    