'''
Created on 10 de mai de 2017

@author: pibic-elloa-nicoli
'''
from sklearn.preprocessing import scale
import random
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
FILENAME = '../../data/files/anninputs/nonnormalizedinputs/01_6.csv'
    
a = pd.read_csv(FILENAME)

#print(a)
#print(scale(a['tsa_09']))
in_a_tsa = np.array(scale(a['tsa_09'].values.reshape(-1,1)))
test_a_tsa = np.array(scale(a['tsa_09'].values.reshape(-1,1)))
print(in_a_tsa)
a['tsa_10'] = scale(a['tsa_10'])
#print('atsa',a[['tsa_09', 'tsa_10']])
std = StandardScaler()
x = std.fit_transform(a['rainfall_01'].values.reshape(-1,1))
print('x',x)
nn = MLPRegressor()
print(len(in_a_tsa), len(x))

nn.fit(in_a_tsa, x.ravel())
y = pd.DataFrame(nn.predict(test_a_tsa))

print(std.inverse_transform(y.values.reshape(-1,1)))


