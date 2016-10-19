# -*- coding: utf-8 -*-
'''
Created on 2 de mai de 2016

@author: Nicoli Araujo
'''

import FromTxtToCSV 
import pandas as pd
import numpy as np

#import seaborn as sns
class CDMFromTxtToCSV(FromTxtToCSV):
    '''
    Vem diretamente do ClimateDataMao.txt original. 
    Gera um arquivo:
        Date    AHT    ALT    ARH    WS    RAINFALL
    1-10-1970   30.8   21.3   89     1.0    29.5
    2-10-1970   34.2   24.3   79.25  6.8    18.2
    3-10-1970   33.9   23.5   75.25  6.17   7
    4-10-1970   34     24.9   80.25  5.0    0
    5-10-1970   33.4   22.8   79     3.1    3.9
    6-10-1970   34.6   25.9   74.5   4.23   0
    
    para cada mês.
    
    Não descarta os nans.
    

    '''
    
    
    
    #def setNewFileData(self, name):
        #with open(name, 'w') as file:
    

    
    def setCollumns(self):
        '''cria listas com os dados retirados do arquivo de entrada para ser manipulados posteriormente'''
        for line in self.OldFileData:
            cont = 0
            fim = 0
            inicio = 0
            for i in line:
                fim +=1
                if (i==";"):
                    cont+=1
                    if (cont == 2):
                        self.colDate.append(line[inicio:fim-1])
                    elif (cont == 5):
                        self.colAHT.append(line[inicio:fim-1])
                    elif (cont == 6):
                        self.colALT.append(line[inicio:fim-1])
                    elif (cont == 7):
                        self.colARH.append(line[inicio:fim-1])
                    elif (cont == 8):
                        self.colWS.append(line[inicio:fim-1])  
                    elif (cont == 4):
                        self.colRainfall.append(line[inicio:fim-1])
                    inicio = fim
    
    def setDateSeparator(self, dateList):
        newDateList = []
        for line in dateList:
            line = str(int(line[:2])) + '-' + str(int(line[3:5])) + '-' + str(int(line[6:]))
            newDateList.append(line)
        return newDateList

    def setDataFrame(self):
        self.dataFrame = pd.DataFrame( {self.labelList[0] : self.colAHT, 
                                        self.labelList[1] : self.colALT, 
                                        self.labelList[2] : self.colARH,     
                                        self.labelList[3] : self.colWS, 
                                        self.labelList[4] : self.colRainfall }, 
                                        index = self.colDate)
        self.dataFrame = self.dataFrame[self.dataFrame.index != '']
        self.dataFrame =self.dataFrame.replace(['', ' '], [np.nan, np.nan])
        self.dataFrame.index.name = 'Date'
        #print(self.dataFrame)
    
    def unifyDates(self):
        '''
        unifica dados de um dia em uma só linha
        '''
        for i in range(0, len(self.colDate)):
            if (self.colDate[i] == self.colDate[i-1]):
                if self.colAHT[i] == '':
                    self.colAHT[i] = self.colAHT[i-1]
                if self.colALT[i] == '':
                    self.colALT[i] = self.colALT[i-1]                
                if self.colARH[i] == '':
                    self.colARH[i] = self.colARH[i-1]
                if self.colWS[i] == '':
                    self.colWS[i] = self.colWS[i-1]
                if self.colRainfall[i] == '':
                    self.colRainfall[i] = self.colRainfall[i-1]
                self.colDate[i-1] = ''  
    
                   
    
    def setData(self, path):
        '''
        pega os dados localizados em path, padroniza e os transfere para um dataFrame
        '''
        self.getOldFileData(path)
        self.removeFirstLines(16)
        self.setCollumns()
        self.truncListNumbers(self.colWS)
        self.colDate = self.setDateSeparator(self.colDate)
        self.unifyDates()
        self.setDataFrame()
            
    def startColumnList(self):
        '''
        Inicializa as listas que conterão cada coluna de dados do dataframe
        '''
        self.colDate = []
        self.colRainfall = []
        self.colWS = []
        self.colARH = []
        self.colALT = []
        self.colAHT = []

    def exportMonth(self, month):
        '''
        exporta os dados de um mês para um arquivo csv - month é um inteiro de 01 a 12
        '''
        (start, end) = self.getLimitYears()
        
        dfExport = pd.DataFrame()
        filename = './Data/files/monthly/RainfallByDay/' + month + 'd.csv'
        lastMonthDay = {'1':'31', '2' : '28', '2B': '29', '3':'31','4':'30','5':'31','6':'30', 
                        '7':'31', '8':'31', '9':'30', '10':'31', '11':'30', '12':'31'}
        with open(filename, 'w') as file:
            
            for year in range(start, end+1):
                startDate = '1-'+ month + '-' + str(year)
                endDate = lastMonthDay[month]+ '-'+ month + '-' + str(year)

                try:
                    if year==start:
                        pd.concat([dfExport,self.dataFrame.loc[startDate:endDate,self.labelList]], axis=1).to_csv(file)
                    else:
                        pd.concat([dfExport,self.dataFrame.loc[startDate:endDate,self.labelList]], axis=1).to_csv(file, header=False)
                except:
                    if year%4 == 0 and month == '2':
                        endDate = lastMonthDay['2B'] + '-'+month + '-' + str(year)
                        if year==start:
                            pd.concat([dfExport,self.dataFrame.loc[startDate:endDate,self.labelList]], axis=1).to_csv(file)
                        else:
                            pd.concat([dfExport,self.dataFrame.loc[startDate:endDate,self.labelList]], axis=1).to_csv(file, header=False)

     
     
                    


    def printMonth(self, month):
        '''
        imprime os dados de um mês 
        '''
        (start, end) = self.getLimitYears()
        lastMonthDay = {'1':'31', '2' : '28', '2B': '29', '3':'31','4':'30','5':'31','6':'30', 
                        '7':'31', '8':'31', '9':'30', '10':'31', '11':'30', '12':'31'}
        for year in range(start, end):
            startDate = '1-'+ month + '-' + str(year)
            endDate = lastMonthDay[month]+ '-'+ month + '-' + str(year)
            try:   
                print(self.dataFrame.loc[startDate:endDate,self.labelList])
            except:
                if year%4 == 0 and month == '2':
                    endDate = lastMonthDay['2B'] + '-'+month + '-' + str(year)
                    print(self.dataFrame.loc[startDate:endDate, self.labelList])
    
    def countEmptyData(self, dataList):
        '''
        Conta quantos dados vazios existem no dataframe e os imprime
        '''
        cont = cont1 = 0
        for i in dataList:
            cont1 +=1
            if i == "":
                cont+=1
        print(cont,cont1)
    
        
    def __init__(self, name):
        '''
        Constructor
        '''
        '''name  =  txt name'''
        self.labelList = ['AHT',     #average highest temperature
                          'ALT',     #average lowest temperature
                          'ARH',     #average relative humidity
                          'WS',      #wind speed
                          'RAINFALL' #precipitação
                          ]
        self.startColumnList()
        self.setData(name)
        #sns.boxplot(x=months,y="RAINFALL", hue="RAINFALL", data=self.dataFrame,palette="Greys")
        #sns.plt.show()'''
        for i in range (1,13):
            self.exportMonth(str(i))
             
        #self.exportMonth('1')
        #self.printMonth('1')
        #print(self.dataFrame.loc['23-1-1995',['AHT','ALT', 'URM', 'WS', 'PRECIPITAÇÃO']])