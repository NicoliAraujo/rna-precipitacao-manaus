'''
Created on 26 de fev de 2017

@author: nicoli
'''
import pandas as pd
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
    
    def __init__(self, result_nets_list, test_data, month, num_nets, source_df_filename):
        self.result_nets_list = result_nets_list
        self.test_data = test_data
        self.month = month
        
        self.source_df_sum = self.read_data_set(source_df_filename).sum()
        
        self.parser_results_anomaly_df_seaborn=pd.DataFrame()
        self.parser_results_df_seaborn = pd.DataFrame()
        self.parser_results_anomaly_volume_df_seaborn = pd.DataFrame()
        self.parser_results_df_volume_seaborn = pd.DataFrame()        
        
        self.results_df = pd.DataFrame()
        self.results_df_volume = pd.DataFrame()
        self.results_anomaly_df = pd.DataFrame()
        self.results_anomaly_volume_df = pd.DataFrame()
        
        self.num_nets = num_nets
        self.start_parser_results_df_seaborn()
        
    def set_parser_results_seaborn(self):
        '''parser do df dos resultados previstos x o encontrado pro seaborn'''
        self.parser_results_df_seaborn = pd.DataFrame(self.test_data['output'])
        self.parser_results_df_seaborn.index = [i for i in range(len(self.test_data['output']))]
        self.parser_results_df_seaborn.rename(columns = {'rainfall_'+str(self.month):'Norm'}, inplace = True)
        self.parser_results_df_seaborn['Year'] = pd.Series(self.test_data['output'].index)
        self.parser_results_df_seaborn['from'] = 'y'
    
        for i in range(self.num_nets):
            results_predict = pd.DataFrame(self.result_nets_list[i].net.predict(self.test_data['input']))
            results_predict.rename(columns = {0:'Norm'}, inplace = True)
            results_predict['Year'] = pd.Series(self.test_data['output'].index)
            results_predict['from'] = 'net_'+str(i)
            self.parser_results_df_seaborn = self.parser_results_df_seaborn.append(results_predict)
    
    def set_seaborn_dfs(self):
        self.set_parser_results_anomaly_df_seaborn()
        self.self.parser_results_anomaly_df_seaborn = self.from_abs_to_anomaly(self.parser_results_df_seaborn, 'Norm')
        self.parser_results_df_volume_seaborn = self.from_norm_to_volume(self.parser_results_df_seaborn)
        self.parser_results_anomaly_volume_df_seaborn = self.from_norm_to_volume_seaborn(self.parser_results_anomaly_df_seaborn)
        
    def save_df(self, filename, df):
        with open(filename, 'w') as file:
            df.to_csv(filename)
    
    def set_results_dfs(self):
        
        self.results_df['y'] = self.test_data['output']
        for i in range(self.num_nets):
            self.results_df['net_'+ str(i)] = self.result_nets_list[i].net.predict(self.test_data['input'])
            self.results_df.index = self.test_data['output'].index
 
        self.results_anomaly_df = self.from_abs_to_anomaly(self.results_df)
        
        self.results_df_volume = self.from_norm_to_volume(self.results_df)
        self.results_anomaly_volume_df = self.from_norm_to_volume(self.results_anomaly_df)
        
    def from_norm_to_volume(self, df_norm):
        '''retorna um df com resultados em volume'''
        return df_norm*self.source_df_sum['rainfall_'+self.month]
    
    def from_abs_to_anomaly(self, abs_df, attr=None):
        if attr==None:
            attr = abs_df.columns
        anomaly_df = abs_df.copy()
        anomaly_df[attr]-=self.results_df['y'].mean()
        return anomaly_df
    
    def from_norm_to_volume_seaborn(self, df_norm):
        df_volume = df_norm.copy()
        df_volume['Norm'] =self.from_norm_to_volume(df_norm)
        return df_volume
    
    def save_results_df(self, filename_norm, filename_norm_anomaly, filename_view, filename_anomaly_view):
        self.save(filename_norm, self.results_df)
        self.save(filename_norm_anomaly,self.results_anomaly_df)
        self.save(filename_view, self.results_df_volume)
        self.save(filename_anomaly_view, self.results_anomaly_volume_df)
        
    def save_results_df_volume(self, filename_seaborn, filename_anomaly_seaborn,filename_norm, filename_norm_anomaly):
        self.save(filename_seaborn, self.parser_results_df_volume_seaborn)
        self.save(filename_anomaly_seaborn, self.parser_results_anomaly_volume_df_seaborn)
        self.save_df(filename_norm, self.parser_results_df_seaborn)
        self.save_df(filename_norm_anomaly, self.parser_results_anomaly_df_seaborn)
        