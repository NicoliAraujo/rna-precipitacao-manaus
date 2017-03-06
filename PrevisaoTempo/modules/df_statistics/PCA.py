# -*- coding: utf-8 -*-
'''
Created on 28 de fev de 2017

@author: nicoli
'''
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns

def my_pca(filename, variable_list):
    all_data = read_data_set(filename)
    
    eval_data = np.array(all_data)
    
    pca = PCA(n_components=3)
    pca.fit(eval_data)
    pca_df_seaborn = pd.DataFrame({'Componente': [], 'Variável': [], 'Valor': []})
    for j in range(len(pca.components_[0])):
        for i in range(len(pca.components_)):
            #print(i, j, all_data.columns[j], pca.components_[i][j])
            #print(pca_df_seaborn)
            pca_df_seaborn = pca_df_seaborn.append({'Componente': i, 
                                   'Variável': all_data.columns[j], 
                                   'Valor': pca.components_[i][j]}, ignore_index=True)
    #print(pca_df_seaborn)
    #[print(row) for row in pca_df_seaborn.index]
    print(len(pca_df_seaborn.index))
    for index in pca_df_seaborn.index:
        #print(index)
        #print(pca_df_seaborn.loc[index, :])
        if pca_df_seaborn['Variável'][index] not in variable_list:
            #print('aaa1', index, pca_df_seaborn, pca_df_seaborn.index[index])
            #pca_df_seaborn = pca_df_seaborn.reindex()
            #print(index)
            pca_df_seaborn.drop(index, axis=0, inplace=True)
            #print('aaa2', index, pca_df_seaborn, pca_df_seaborn.index[index])
    print(len(pca_df_seaborn.index))
    pca_df_seaborn = pca_df_seaborn.loc[pca_df_seaborn['Componente']==0]
    plot_pca(pca_df_seaborn)
    
    
def plot_pca(pca_df):
    g = sns.factorplot(x='Variável', y = 'Valor', size = 15, aspect = 5,
               data=pca_df, kind="bar")
    g.despine(left=True)
    g.set_ylabels("Results")
    #sns.plt.savefig('../../data/images/predictanalysis/' + '01' + type + '.png')
    sns.plt.savefig('../../data/images/pca/ninotsa.png')

def read_data_set(filename):
    return pd.read_csv(filename, sep=r',', index_col=0)
if __name__ == '__main__':
    PATH_INPUT = '../../data/files/original/AllNormalizedData.csv'
#     variable_list = ['rainfall_01', 'rainfall_02', 'rainfall_03', 'rainfall_04',
#        'rainfall_05', 'rainfall_06', 'rainfall_07', 'rainfall_08',
#        'rainfall_09', 'rainfall_10', 'rainfall_11', 'rainfall_12', 'nino12_01',
#        'nino12_02', 'nino12_03', 'nino12_04', 'nino12_05', 'nino12_06',
#        'nino12_07', 'nino12_08', 'nino12_09', 'nino12_10', 'nino12_11',
#        'nino12_12', 'nino3_01', 'nino3_02', 'nino3_03', 'nino3_04', 'nino3_05',
#        'nino3_06', 'nino3_07', 'nino3_08', 'nino3_09', 'nino3_10', 'nino3_11',
#        'nino3_12', 'nino34_01', 'nino34_02', 'nino34_03', 'nino34_04',
#        'nino34_05', 'nino34_06', 'nino34_07', 'nino34_08', 'nino34_09',
#        'nino34_10', 'nino34_11', 'nino34_12', 'nino4_01', 'nino4_02',
#        'nino4_03', 'nino4_04', 'nino4_05', 'nino4_06', 'nino4_07', 'nino4_08',
#        'nino4_09', 'nino4_10', 'nino4_11', 'nino4_12', 'tsa_01', 'tsa_02',
#        'tsa_03', 'tsa_04', 'tsa_05', 'tsa_06', 'tsa_07', 'tsa_08', 'tsa_09',
#        'tsa_10', 'tsa_11', 'tsa_12']
    variable_list = ['rainfall_01','nino12_01',
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
       'tsa_10', 'tsa_11', 'tsa_12']
    #PATH_INPUT = '../../data/files/anninputs/regularinputs/01_6.csv'
    my_pca(PATH_INPUT, variable_list)
    
    '''
    quais sao os meses mais importantes
    encontrar variáveis mais importantes: volume rio, temperatura máxima/mínima, variáveis regionais
    '''
    