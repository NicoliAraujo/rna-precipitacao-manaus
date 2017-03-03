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
    #print(len(all_data))
    eval_data = np.array(np.transpose(all_data))
    print(len(eval_data))
    pca = PCA(n_components=72)
    pca.fit(eval_data)
    print(pca.components_)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    print('pca ')
    print(pca.explained_variance_ratio_.sum(), len(pca.explained_variance_ratio_))
    dict = {}
    i=0
    print(all_data.columns, len(all_data.columns))
    for name in all_data.columns:
        print(name, i)
        dict[name] = pca.explained_variance_ratio_[i]
        i+=1
    
    #pca.components_ = np.absolute(pca.components_)
    #result = np.sum(pca.components_,axis = 0)
#     print(result)
#     for i in range(0,len(result)):
#         if(result[i]>=2.5):
#             print(i)
    #plot_pca(pca.components_)
    
def plot_pca(pca_components):
    g = sns.factorplot(x=pca_components, size = 8, aspect = 3,
               kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Results")
    #sns.plt.savefig('../../data/images/predictanalysis/' + '01' + type + '.png')
    sns.plt.savefig('../../data/images/pca/pca.pdf')

def read_data_set(filename):
    return pd.read_csv(filename, sep=r',', index_col=0)
if __name__ == '__main__':
    PATH_INPUT = '../../data/files/original/AllData.csv'
    my_pca(PATH_INPUT, ['rainfall_01', 'nino12_01'])
    