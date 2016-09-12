# -*- coding: utf-8 -*-
'''
Created on 12 de set de 2016

@author: Nicoli Araujo
'''
import pandas as pd
import numpy as np

class FromTxtToCSV():
    def getOldFileData(self, path):
        '''abre o arquivo de entrada'''
        with open(path, 'r', encoding = 'latin-1') as file:
            self.OldFileData = file.read().splitlines()
                       
    def truncListNumbers(self, list):
        '''
        trunca os números da lista dada para apenas 2 casas decimais
        '''
        for i in range(0, len(list)):
            if list[i] != '':
                list[i] = np.round(float(list[i]),2)
                
    def removeFirstLines(self, line):
        '''remove as primeiras linhas do arquivo - as que não tem dados'''
        for i in range(0,line): 
            self.OldFileData.pop(0)
            
             
    def getLimitYears(self):
        newestYear = 1900
        oldestYear = 5000
        for date in self.dataFrame.index:
            year = int(date[-4:])
            if year >= newestYear:
                newestYear = year
            if year <= oldestYear:
                oldestYear = year
        return (oldestYear,newestYear)
    
class MMFromTxtToCSV(FromTxtToCSV):
    
    def __init__(self, path):
        self.getOldFileData(path)
        #print(self.OldFileData)
    
    def replaceSeparator(self, sepList):
        for sep in sepList:
            for i in range(len(self.OldFileData)):
                self.OldFileData[i] = self.OldFileData[i].replace(sep, ';')
                
        #print(self.OldFileData)
        
    def insertLastComma(self):
        for i in range(len(self.OldFileData)):
            self.OldFileData[i] += ';'
            
        
    def startCollumnDict(self):
        self.ColumnDict = {}
        self.ColumnDict['Year'] = []
        for i in range(1, 13):
            self.ColumnDict[i] = []
       
    def setCollumns(self):
        self.startCollumnDict()
        for i in range(len(self.OldFileData)):
            cont = 0
            fim = 0
            inicio = 0
            line = self.OldFileData[i]
            for j in range(len(line)):
                letter = line[j]
                fim +=1
                if (letter == ";"):
                    
                    word = line[inicio:fim-1]
                    #print(i, word)
                    if (cont == 0):
                        self.ColumnDict['Year'].append(int(word))
                    elif (cont<13):
                        #print(cont, word)
                        self.ColumnDict[cont].append(float(word))
                    cont+=1
                    inicio = fim
                    
        #self.printColumnDict()
        
    def printColumnDict(self):
        for key in self.ColumnDict:
            print(key, len(self.ColumnDict[key]), self.ColumnDict[key])
        print('\n')
    
    
    def setDataFrame(self):
        #print(self.ColumnDict)
        self.dataFrame = pd.DataFrame( {key : self.ColumnDict[key] for key in range(1, 13)}, 
                                       index = self.ColumnDict['Year'])
        #self.dataFrame = self.dataFrame[self.dataFrame.index != '']
        #self.dataFrame =self.dataFrame.replace(['', ' '], [np.nan, np.nan])
        self.dataFrame.index.name = 'Year'
        #print(self.dataFrame)
    
    def setCSV(self, sepList, name):
        #print(self.OldFileData)
        self.replaceSeparator(sepList)
        #print(self.OldFileData)
        self.insertLastComma()
        self.setCollumns()
        self.setDataFrame()
        self.saveCSV(name)
        #print(self.ColumnDict)
    
    def saveCSV(self, name):
        newpath = '../../data/original/csv/' + name + '.csv'
        with open(newpath, 'w') as file:
            self.dataFrame.to_csv(file)
            
if __name__ == '__main__':
    path = '../../data/original/other/manaus_mensal.txt'
    manaus_mensal = MMFromTxtToCSV(path)
    manaus_mensal.setCSV(['\t'], 'manaus_mensal')
    
    path = '../../data/original/other/nino1+2.txt'
    nino12 = MMFromTxtToCSV(path)
    nino12.setCSV(['  '], 'nino12')
    
    path = '../../data/original/other/nino3.txt'
    nino3 = MMFromTxtToCSV(path)
    nino3.setCSV(['  '], 'nino3')
    
    path = '../../data/original/other/nino34.txt'
    nino34 = MMFromTxtToCSV(path)
    nino34.setCSV(['  '], 'nino34')
    
    path = '../../data/original/other/nino4.txt'
    nino4 = MMFromTxtToCSV(path)
    nino4.setCSV(['  '], 'nino4')
    
    
    path = '../../data/original/other/tsa.txt'
    tsa = MMFromTxtToCSV(path)
    tsa.setCSV(['    ', '   '], 'tsa')

         