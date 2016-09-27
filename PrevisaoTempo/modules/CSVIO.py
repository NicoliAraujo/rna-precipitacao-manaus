'''
Created on 26 de set de 2016

@author: pibic-elloa-nicoli
'''
from pandas.io.tests.parser import index_col
from unittest.mock import inplace

'''class CSVIO(object):
    
    #classdocs
    
    

    def __init__(self):
        
        #Constructor
        
        
        '''
from FromTxtToCSV import MMFromTxtToCSV
from DataStatistics import Anomaly
import pandas as pd

class JointDataFrame():
    '''colocar toda a parte de juntar os dataframes aqui: 
    1) chamar original do .txt
    2) chamar anomalies
    3) editar limites de anos
    4) colocar tudo num df só
    5) salvar
    ''' 
    def setOriginal(self, path, sepList, name):
        x = MMFromTxtToCSV(path)
        x.setCSV(sepList, name)
        return x.dataFrame
    
    def setAnomalies(self, name):
        a = Anomaly(name)
        a.setAnomalyDF()
        return a.anomalyDF
    
    def setYears(self, df, lim1, lim2):
        df = df[df.index >= lim1]
        df = df[df.index <= lim2]
        return df
    
    def setdfColName(self,name):
        namelist = []
        #print(self.dfDict[name])
        for collumn in self.dfDict[name]:
            namelist.append(collumn)
            #print(namelist, collumn)
        for i in range(len(namelist)):
            #print(collumn)
            namelist[i] = name + '_' + namelist[i]
        #print(namelist)
        self.dfDict[name].columns = namelist
        
    def join(self):
        
        for name in self.datasequencelist:
            self.Joindf = pd.concat([self.Joindf, self.dfDict[name]], axis=1)
        print(self.Joindf)
    
    def setJoinDict(self):
        self.dfDict = {}
        for key in self.dataDict:
            #print(key)
            path = self.dataDict[key][0]
            sep = self.dataDict[key][1]
            name = self.dataDict[key][2]
            #print(path, sep, name)
            #1) pegar os original
            df = self.setOriginal(path, sep, name)
            #)setar anomalias
            df = self.setAnomalies(name)
            #3)setar anos
            df = self.setYears(df, 1950, 2015)

            self.dfDict[name] = df
            #setar colunas
            self.setdfColName(name)
    
        
        #print(self.dfDict)
    def saveJoin(self):
        with open('../data/files/anomalydata/AllAnomalyData.csv', 'w') as file:
            self.Joindf.to_csv(file)
            
    def __init__(self, dataDict, datasequencelist):
        self.dataDict = dataDict
        self.datasequencelist = datasequencelist
        self.setJoinDict()
        #print(self.dfDict[])
        #print(self.dfDict['rainfall'].columns)
        #print(self.dfDict['rainfall'])
        self.Joindf = pd.DataFrame()
        #self.join(self.dfDict)
        
if __name__ == '__main__':
    DataDict = {'manaus_mensal': ['../data/original/other/rainfall.txt', ['\t'], 'rainfall'],
                'nino12': ['../data/original/other/nino1+2.txt', ['  '], 'nino12'],
                'nino3': ['../data/original/other/nino3.txt', ['  '], 'nino3'],
                'nino34':['../data/original/other/nino34.txt', ['  '], 'nino34'], 
                'nino4': ['../data/original/other/nino4.txt', ['  '], 'nino4'],
                'tsa':['../data/original/other/tsa.txt', ['    ', '   '], 'tsa']}
    a = JointDataFrame(DataDict, datasequencelist=['rainfall', 'tsa', 'nino12', 'nino3', 'nino34', 'nino4'])
    
    #a.setJointDict()
    #print(self.dfDict[])
    #print(self.dfDict['rainfall'].columns)
    #print(self.dfDict['rainfall'])
    
    a.join()
    a.saveJoin()
