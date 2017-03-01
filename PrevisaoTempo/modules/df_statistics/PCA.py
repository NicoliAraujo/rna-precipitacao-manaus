# -*- coding: utf-8 -*-
'''
Created on 28 de fev de 2017

@author: nicoli
'''
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns

def my_pca(filename):
    all_data = np.array(read_data_set(filename))
    pca = PCA(n_components=5)
    pca.fit(all_data)
    pca.components_ = np.absolute(pca.components_)
    result = np.sum(pca.components_,axis = 0)
    print(result)
    for i in range(0,len(result)):
        if(result[i]>=2.5):
            print(i)

def plot_pca(mydata):
    g = sns.factorplot(x='Year', y='Norm', hue = 'from', data=mydata, size = 8, aspect = 3,
               kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Results")
    #sns.plt.savefig('../../data/images/predictanalysis/' + '01' + type + '.png')
    sns.plt.savefig('../../data/images/pca/pca.pdf')

def read_data_set(filename):
    return pd.read_csv(filename, sep=r',', index_col=0)
if __name__ == '__main__':
    PATH_INPUT = '../../data/files/original/AllData.csv'
    my_pca(PATH_INPUT)