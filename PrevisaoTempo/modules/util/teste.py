'''
Created on 26 de fev de 2017

@author: nicoli
'''
import random
import pandas as pd
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae

x = [random.randrange(10) for i in range(10)]
y = [random.randrange(10) for i in range(10)]
z = [random.randrange(10) for i in range(10)]

df1 = pd.DataFrame({'x': x, 'y': y, 'z': z})

a = [random.random() for i in range(10)]
b = [random.random() for i in range(10)]
c = [random.random() for i in range(10)]

df2 = pd.DataFrame({'a': x, 'b': y, 'c': z})

mlp1 = MLPRegressor(solver='lbfgs', early_stopping=True)
mlp2 = MLPRegressor(solver='lbfgs', early_stopping=True)

mlp1 = mlp1.fit(df1[['x','y']][0:8], df1['z'][0:8])
mlp2 = mlp2.fit(df2[['a','b']][0:8], df2['c'][0:8])

result1 = mlp1.predict(df1[['x','y']][8:10])
result2 = mlp2.predict(df2[['a','b']][8:10])

dif1 = abs(df1['z'][8:10] - abs(result1))/df1['z'][8:10]
mymape1 = 100/len(result1) * dif1.sum()

dif2 = abs(df2['c'][8:10] - abs(result2))/df2['c'][8:10]
mymape2 = 100/len(result2) * dif2.sum()


print('mymape1', mymape1)
print('mymape2', mymape2)

mae1 = mae(df1['z'][8:10], result1)
mape1 = 100*mae1

mae2 = mae(df2['c'][8:10], result2)
mape2 = 100*mae2

print('mape1', mape1)
print('mape2', mape2)

print('mae1', mae1)
print('mae2', mae2)

mse1 = mse(df1['z'][8:10], result1)
mse2 = mse(df2['c'][8:10], result2)

print('mse1', mse1)
print('mse2', mse2)
