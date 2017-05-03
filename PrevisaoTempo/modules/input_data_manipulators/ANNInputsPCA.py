'''
Created on 26 de abr de 2017

@author: pibic-elloa-nicoli
'''

from sklearn.decomposition import PCA

#from modules.util.FromPandasToLatex import save_dataset as save
#import numpy as np
import pandas as pd


class ANNInputsPCA():
    '''Classe que cria e salva os datasets com os pcas para servir de entrada para as redes neurais
    '''
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0)
    
    def __init__(self, filename_original, n_components):
        self.my_n_components = n_components
        self.df_original = self.read_data_set(filename_original)
        #print(self.df_original)
        self.pca = PCA(svd_solver='full', n_components=self.my_n_components)
        self.pca_df = pd.DataFrame({col_name: [] for col_name in self.df_original.columns})
        self.new_df_pca = pd.DataFrame()
    def get_pca(self):
        self.pca.fit(self.df_original)
        self.set_pca_df()
        self.new_df_pca = pd.DataFrame(self.pca.transform(self.df_original), 
                                       columns = ['pca_'+str(i) for i in range(1, self.my_n_components+1)],
                                       index = self.df_original.index)
        print('new df pca \n', self.new_df_pca)
        #print(len(self.new_df_pca), len(self.new_df_pca[0]))
    
    
    def set_pca_df(self):
        for i in range(len(self.pca.components_)):
            #print(pca.components_[i])
            j=0
            dict={}
            for col_name in self.df_original.columns:
                #print(col_name,pca.components_[i][j])
                dict[col_name] = self.pca.components_[i][j]
                j+=1
            self.pca_df = self.pca_df.append(dict, ignore_index=True)
        self.pca_df=self.pca_df.reindex(columns=['rainfall_01', 'rainfall_07', 'rainfall_08',
        'rainfall_09', 'rainfall_10', 'rainfall_11', 'rainfall_12',
       'nino12_07', 'nino12_08', 'nino12_09', 'nino12_10', 'nino12_11',
       'nino12_12',  'nino3_07', 'nino3_08', 'nino3_09', 'nino3_10', 'nino3_11',
       'nino3_12', 'nino34_07', 'nino34_08', 'nino34_09',
       'nino34_10', 'nino34_11', 'nino34_12', 'nino4_07', 'nino4_08',
       'nino4_09', 'nino4_10', 'nino4_11', 'nino4_12', 'tsa_07', 'tsa_08', 'tsa_09',
       'tsa_10', 'tsa_11', 'tsa_12'])
        #print('pca df\n', self.pca_df)
        

    def save_df(self, filename, df):
        with open(filename, 'w') as file:
            df.to_csv(filename)
    
if __name__ == '__main__':
    FILENAME = '../../data/files/anninputs/normalizedinputs/01_6.csv'
    
    n_pcs=18
    rc = ANNInputsPCA(FILENAME, n_pcs)
    rc.get_pca()
    rc.save_df('../../data/files/anninputs/pca_inputs/01_6_'+str(n_pcs)+'pcs.csv', rc.new_df_pca)
    #rc.set_pca_df()
    

    