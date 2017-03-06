'''
Created on 29 de dez de 2016

@author: nicoli
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from numpy import int8, float64
class To_Seaborn():
    def __init__(self, filename):
        self.dataset = self.read_data_set(filename)
        #print(self.dataset)
        
        
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(10)
    
    def get_variable_dataset(self, variable, my_x, my_y):
        for column in self.dataset.columns:
            if column[:-3] != variable:
                self.dataset.drop(column, axis=1, inplace=True)
        variable_data_set = pd.DataFrame({my_x: np.zeros(len(self.dataset)*len(self.dataset.transpose()),  dtype=int8), 
                                          my_y: np.zeros(len(self.dataset)*len(self.dataset.transpose()), dtype=float64)})
        #print(variable_data_set)
        self.dataset.rename(columns={col:col.replace(variable+'_', '') for col in self.dataset.columns}, inplace=True)
        self.dataset.rename(columns={col:int(col) for col in self.dataset.columns}, inplace=True)

        i=0
        #print(self.dataset)
        for column in self.dataset.columns:
            for index in self.dataset.index:
                #print(column, self.dataset[column][index])
                
                variable_data_set.set_value(i, my_x, column)
                variable_data_set.set_value(i, my_y, self.dataset[column][index])
                i+=1
        #print(variable_data_set)
        self.plot_grafico(variable_data_set, my_x, my_y, variable)
    def plot_grafico_box(self, dataset, my_x, my_y, variable):
        my_palette = sns.diverging_palette(255, 133, l=60, n=12, center="light")
        with sns.plotting_context("talk", font_scale=1.5):
            
            sns.set_style("whitegrid")
            plt.figure(figsize=(17, 8))
            self.g = sns.boxplot(x=my_x, y = my_y, data=dataset,
                       color='greenyellow')
    def set_violin_dataset(self):
        violin_data_set = pd.DataFrame({'Mês': [], 'Variável': [], 'Valor': [], 'Ano': []})
        for index in self.dataset.index:
            for col in self.dataset.columns:
                #print(col)
                violin_data_set = violin_data_set.append({'Mês': int(col[-2:]), 
                                   'Variável': col[:-3], 
                                   'Valor': self.dataset[col][index],
                                   'Ano': index}, ignore_index=True)
        
    
    def save_csv(self, file_csv):
        filename = '../../data/files/original/AllNormalizedSeabornData.csv'
        with open(filename, 'w') as file:
            file_csv.to_csv(file, sep = r',')
    
    def plot_grafico_violino(self, my_x, my_y):
        with sns.plotting_context("talk", font_scale=1.5):
            
            sns.set_style("whitegrid")
            plt.figure(figsize=(17, 8))
            self.g = sns.violinplot(x=my_x, y=my_y, data=self.dataset, split=True,
               inner="quart")   
        
            
            sns.plt.savefig('../../data/images/analise_variaveis/violin_plot' + my_x + '_' + my_y +  '.png')
            
    def set_violin_month_data_set(self, mes):
        for index in self.dataset:
            self.dataset.drop(column, axis=1, inplace=True)
    
if __name__ == '__main__':
    #print('oier')
#     MONTH = '01'
#     TIME_GAP = '12'
#     EXTENSION = 'csv'
    #ETC = '_regression_dataset_normalized'
#     ETC = '_inputs'
    #PATH_INPUT = '../../data/files/ann_output_files/' + MONTH + '_' + TIME_GAP  + ETC + '.csv'
    #PATH_INPUT = '../../data/files/original/AllData.csv'
    PATH_INPUT = '../../data/files/original/AllNormalizedData.csv'
    #PATH_INPUT = '../../data/files/ann_output_files/01_6_regression_dataset_normalized.csv'
    #PATH_INPUT = '../../data/files/anninputs/nonnormalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    #PATH_OUTPUT = '../../data/files/latex/' + 'tabela' + MONTH + '_' + TIME_GAP + ETC + '.tex'
    #PATH_OUTPUT = '../../data/files/latex/' + 'tabela' + MONTH + '_' + TIME_GAP + ETC + '.tex'
    #jan = To_Seaborn(PATH_INPUT)
    #jan.get_variable_dataset('nino3', 'Mês', 'Niño 3')
    #PATH_INPUT = '../../data/files/original/AllNormalizedSeabornData.csv'
    violin = To_Seaborn(PATH_INPUT)
    #violin_data_set = violin.set_violin_dataset()
    violin.plot_grafico_violino('Variável', 'Valor')
    