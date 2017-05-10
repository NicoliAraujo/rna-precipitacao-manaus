# -*- coding: utf-8 -*-
'''
Created on 26 de set de 2016
@author: pibic-elloa-nicoli
'''
# from FromTxtToCSV import MMFromTxtToCSV, Rainfall2008_2015
# from df_statistics.DataStatistics import Anomaly
from sklearn.preprocessing import scale

import pandas as pd


class JoinData():
    '''colocar toda a parte de juntar os dataframes aqui:
    1) chamar original do .txt
    2) chamar anomalies
    3) editar limites de anos
    4) colocar tudo num df só
    5) salvar
    '''

    '''    def set_txt_original(self, path, sep_list, name):
        ''' '''
        parser_txt_csv = MMFromTxtToCSV(path)
        parser_txt_csv.set_csv(sep_list, name)
        parser_txt_csv.save_csv(name)
        return parser_txt_csv.data_frame'''

    '''def set_anomalies(self, name):
        ''' '''
        parser_anomaly = Anomaly(name)
        parser_anomaly.set_anomaly_df()
        return parser_anomaly.anomaly_df'''

    def set_years(self, data_frame, lim1, lim2):
        data_frame = data_frame[data_frame.index >= lim1]
        data_frame = data_frame[data_frame.index <= lim2]
        return data_frame

    def set_df_col_name(self, df_dict, name):
        namelist = []
        # print(self.dfDict[name])
        for collumn in df_dict[name]:
            namelist.append(collumn)
            # print(namelist, collumn)
        for i in range(len(namelist)):
            # print(collumn)
            namelist[i] = name + '_' + namelist[i]
        # print(namelist)
        df_dict[name].columns = namelist
        return df_dict
    
    '''def set_rainfall_data_frame(self):
        rainfall_2008_2015_anomaly = Anomaly('rainfall_2008_2015')
        rainfall_2008_2015_anomaly.set_anomaly_df()
        self.join_df.update(rainfall_2008_2015_anomaly.anomaly_df)
'''
    def join(self):
        '''concatena os dataframes desejados'''
        for name in self.data_sequence_list:
            self.join_df = pd.concat([self.join_df, self.df_dict[name]], axis=1)
        # self.set_rainfall_data_frame()
        for l in self.join_df.columns:
            self.join_df[l] = scale(self.join_df[l])
        print(self.join_df)

    def set_join_dict(self, data_dict):
        '''formata um dicionário de dataframes com os dados inputados no main'''
        df_dict = {}
        for key in self.data_dict:
            # print(key)
            
            path = data_dict[key]
            sep = r','
            name = key
            # print(path, sep, name)
            # 1) pegar os csv original
            data_frame = pd.read_csv(path, sep, index_col=0)
            print(key, data_frame)
            # )setar anomalias
            # data_frame = self.set_anomalies(name)
            # 3)setar anos
            data_frame = self.set_years(data_frame, 1950, 2015)

            df_dict[name] = data_frame
            # setar colunas
            df_dict = self.set_df_col_name(df_dict, name)
        return df_dict
        # print(self.dfDict)
    def save_join(self):
        '''salva o df gerado em um csv'''
        with open('../../data/files/original/csv/AllStdData.csv', 'w') as file:
            self.join_df.to_csv(file)

    def __init__(self, data_dict, data_sequence_list):
        self.data_dict = data_dict
        self.data_sequence_list = data_sequence_list
        # print(self.data_sequence_list)
        self.df_dict = self.set_join_dict(self.data_dict)
        # print(self.df_dict)
        # print(self.dfDict['rainfall'].columns)
        # print(self.dfDict['rainfall'])
        self.join_df = pd.DataFrame()
        # self.join(self.dfDict)

if __name__ == '__main__':
    DATA_DICT = {'rainfall':'../../data/files/original/csv/rainfall_1925_2015.csv',
                 # 'rainfall2008_2015': ['../../data/files/original/other/chuvaMensal2008_2015.txt', ['\t'], 'rainfall2008_2015'],
                 'nino12': '../../data/files/original/csv/nino12.csv',
                 'nino3': '../../data/files/original/csv/nino3.csv',
                 'nino34':'../../data/files/original/csv/nino34.csv',
                 'nino4': '../../data/files/original/csv/nino4.csv',
                 'tsa':'../../data/files/original/csv/tsa.csv'}
    DATA_SEQUENCE_LIST = ['rainfall', 'nino12', 'nino3', 'nino34', 'nino4', 'tsa']
    JOIN = JoinData(DATA_DICT, DATA_SEQUENCE_LIST)
    
    JOIN.join()
    JOIN.save_join()
    
