'''
Created on 26 de abr de 2017

@author: pibic-elloa-nicoli
'''

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

from modules.util.FromPandasToLatex import save_dataset as save

def read_data_set(filename):
    return pd.read_csv(filename, sep=r',', index_col=0)


if __name__ == '__main__':
    dataset = read_data_set('../../data/files/original/csv/AllData.csv')
    #print(len(dataset))
    pca = PCA(svd_solver='full', n_components=10)
    #print(dataset)
    pca.fit(dataset)
    #print(pca.components_,len(pca.components_), len(pca.components_[0]))
    #print(len(pca.components_))
    pca_df = pd.DataFrame({col_name: [] for col_name in dataset.columns})
    for i in range(len(pca.components_)):
        #print(pca.components_[i])
        j=0
        dict={}
        for col_name in dataset.columns:
            #print(col_name,pca.components_[i][j])
            dict[col_name] = pca.components_[i][j]
            j+=1
        pca_df = pca_df.append(dict, ignore_index=True)
            
    #print(pca_df['rainfall_01'])
    pca_df=pca_df.reindex(columns=['rainfall_01',  'rainfall_02', 'rainfall_03', 'rainfall_04',
       'rainfall_05', 'rainfall_06', 'rainfall_07', 'rainfall_08',
        'rainfall_09', 'rainfall_10', 'rainfall_11', 'rainfall_12','nino12_01',
       'nino12_02', 'nino12_03', 'nino12_04', 'nino12_05', 'nino12_06',
       'nino12_07', 'nino12_08', 'nino12_09', 'nino12_10', 'nino12_11',
       'nino12_12', 'nino3_01', 'nino3_02', 'nino3_03', 'nino3_04', 'nino3_05',
       'nino3_06', 'nino3_07', 'nino3_08', 'nino3_09', 'nino3_10', 'nino3_11',
       'nino3_12', 'nino34_01', 'nino34_02', 'nino34_03', 'nino34_04',
       'nino34_05', 'nino34_06', 'nino34_07', 'nino34_08', 'nino34_09',
       'nino34_10', 'nino34_11', 'nino34_12', 'nino4_01', 'nino4_02',
       'nino4_03', 'nino4_04', 'nino4_05', 'nino4_06', 'nino4_07', 'nino4_08',
       'nino4_09', 'nino4_10', 'nino4_11', 'nino4_12', 'tsa_01', 'tsa_02',
       'tsa_03', 'tsa_04', 'tsa_05', 'tsa_06', 'tsa_07', 'tsa_08', 'tsa_09',
       'tsa_10', 'tsa_11', 'tsa_12'])
    print(pca_df)
    print(pca.transform(dataset))
    
    #save(pca_df, '../../data/files/latex/pca/pca.tex')
    
    
    