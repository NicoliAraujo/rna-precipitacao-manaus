# -*- coding: utf-8 -*-
'''
Created on 28 de fev de 2017

@author: nicoli
'''


from sklearn.decomposition import PCA

import numpy as np
import pandas as pd


data_set = pd.read_csv('../files/db_pca.csv', index_col=0)
data_set = np.array(data_set)
pca = PCA(n_components=20)
pca.fit(data_set)
pca.components_ = np.absolute(pca.components_)
result = np.sum(pca.components_, axis=0)
for i in range(0, len(result)):
    if(result[i] >= 2.5):
        print(i)
