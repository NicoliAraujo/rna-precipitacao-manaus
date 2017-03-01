'''
Created on 26 de fev de 2017

@author: nicoli
'''
import pandas as pd
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
 
        self.predict_anomaly_df = self.predict_df.copy()
        self.predict_anomaly_df-=self.predict_df['y'].mean()
        
    def set_predict_df_seaborn(self):
        for i in range(self.num_nets):
            results_predict = pd.DataFrame(self.result_nets_list[i].net.predict(self.test_data['input']))
            results_predict.rename(columns = {0:'Norm'}, inplace = True)
            results_predict['Year'] = pd.Series(self.test_data['output'].index)
            results_predict['from'] = 'net_'+str(i)
            self.predict_df_seaborn = self.predict_df_seaborn.append(results_predict)
        
        self.predict_anomaly_df_seaborn = self.predict_df_seaborn.copy()
        self.predict_anomaly_df_seaborn['Norm']-=self.predict_df['y'].mean()
    
    
    def save_predict_df(self, filename_norm, filename_norm_anomaly):
        with open(filename_norm, 'w') as file:
            self.predict_df.to_csv(filename_norm)
        with open(filename_norm_anomaly, 'w') as file:
            self.predict_anomaly_df.to_csv(filename_norm_anomaly)
        
    def save_predict_df_seaborn(self, filename_norm, filename_norm_anomaly):
        with open(filename_norm, 'w') as file:
            self.predict_df_seaborn.to_csv(filename_norm)
        with open(filename_norm_anomaly, 'w') as file:
            self.predict_anomaly_df_seaborn.to_csv(filename_norm_anomaly)

    def start_predict_dfs_volume(self, filename):
        self.source_df_sum = self.read_data_set(filename).sum()
        
        self.predict_df_volume = self.predict_df*self.source_df_sum['rainfall_'+self.month]
        
        self.predict_df_volume_seaborn  =self.predict_df_seaborn.copy()
        self.predict_df_volume_seaborn['Norm']*=self.source_df_sum['rainfall_'+self.month]
        
        self.predict_anomaly_df_volume = self.predict_anomaly_df*self.source_df_sum['rainfall_'+self.month]
        
        self.predict_anomaly_df_volume_seaborn = self.predict_anomaly_df_seaborn.copy()
        self.predict_anomaly_df_volume_seaborn['Norm']*= self.source_df_sum['rainfall_'+self.month]
        
    
    def save_predict_df_volume(self, filename_seaborn, filename_view, filename_anomaly_seaborn, filename_anomaly_view):
        with open(filename_seaborn, 'w') as file:
            self.predict_df_volume_seaborn.to_csv(filename_seaborn)
        with open(filename_view, 'w') as file:
            self.predict_df_volume.to_csv(filename_view)
        with open(filename_anomaly_view, 'w') as file:
            self.predict_anomaly_df_volume.to_csv(filename_anomaly_view)
        with open(filename_anomaly_seaborn, 'w') as file:
            self.predict_anomaly_df_volume_seaborn.to_csv(filename_anomaly_seaborn)
        
