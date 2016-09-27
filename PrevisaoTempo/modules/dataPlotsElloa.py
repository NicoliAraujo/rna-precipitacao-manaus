# Graficos das relações entre variáveis indepentes e variável dependente
# Elloá B. Guedes  - 26/03/2016

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Abrindo o arquivo
ourData = pd.read_csv("./dados/1.csv", sep=r",")
print(ourData)
print(ourData["PRECIPITACAO"])

# Strip plot da temperatura maxima versus rainfall 
#sns.stripplot(y="AHT", x="rainfall", data=ourData, jitter=True,palette="Greys")#
#sns.plt.show()

# Boxplot de AHT versus rainfall -- Já no artigo
sns.boxplot(x="PRECIPITACAO", y="AHT", hue="PRECIPITACAO", data=ourData,palette="Greys");
sns.plt.show()

# Boxplot dos dados de entrada -- Já no artigo!
#sns.boxplot(ourData[['AHT','ALT']],palette="Greys")
#sns.plt.show()

# Explorando rainfall
'''
print(ourData['rainfall'].value_counts()) # qtde dias que choveram e nao choveram
ourData = pd.read_csv("text_data4.txt", sep=r"\s+")
rainfallLastYear = (ourData['rainfall'])[-365:]
# sns.countplot(x="rainfall", data=ourData, palette="Greys") # melhor mostrar com texto
sns.tsplot(rainfallLastYear)
sns.plt.show()'''

# Teste Chi-Quadrado para Rainfall
#import scipy.stats as scp
#observed = [5889, 5830]
#print(scp.chisquare(observed))
'''
# Stem plot do último mês de chuva
ourData = pd.read_csv("text_data4.txt", sep=r"\s+")
rainfallLastYear = (ourData['rainfall'])[-30:]
newList = []
for i in rainfallLastYear:
    if i == 0:
        newList += [0]
    else:
        newList += [1]
        
print(newList)

from pylab import *
listX = []
for i in range(1,30 + 1):
    listX += [i]
    
plt.axis((0,31,-0.2,1.2))
markerline, stemlines, baseline = stem(listX, newList, '-', bottom=-0.2)
setp(stemlines, linewidth=0.5, color="black")
setp(markerline, markerfacecolor="black")
setp(baseline, 'color','black', 'linewidth', 2)
show()'''