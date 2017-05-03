# -*- coding: utf-8 -*-
'''
Created on 12 de set de 2016

@author: Nicoli Araujo
'''
from datetime import date

import numpy as np
import pandas as pd


class FromTxtToCSV():
    '''pega um arquivo txt com dados e o transforma em .csv'''
    def get_old_file_data(self, filepath):
        '''abre o arquivo de entrada'''
        with open(filepath, 'r', encoding='latin-1') as file:
            return file.read().splitlines()

    def trunc_list_numbers(self, trunc_list):
        '''
        trunca os números da lista dada para apenas 2 casas decimais
        '''
        for i in range(0, len(trunc_list)):
            if trunc_list[i] != '':
                trunc_list[i] = np.round(float(trunc_list[i]), 2)

    def remove_first_lines(self, line):
        '''remove as primeiras linhas do arquivo - as que não tem dados'''
        for i in range(0, line):
            self.old_file_data.pop(0)

    def get_limit_years(self):
        newest_year = 1900
        oldest_year = 5000
        for date in self.data_frame.index:
            year = int(date[-4:])
            if year >= newest_year:
                newest_year = year
            if year <= oldest_year:
                oldest_year = year
        return (oldest_year, newest_year)


class MMFromTxtToCSV(FromTxtToCSV):
    '''doc'''
    def __init__(self, filepath):
        '''Constructor'''
        self.keylist = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.old_file_data = self.get_old_file_data(filepath)
        self.data_frame = pd.DataFrame()
        self.column_dict = self.start_collumn_dict()

        #print(self.old_file_data)

    def replace_separator(self, sep_list):
        '''muda o separador pra ser uma ;'''
        for sep in sep_list:
            #print(sep)
            for i in range(len(self.old_file_data)):
                self.old_file_data[i] = self.old_file_data[i].replace(sep, ';')
        #print(self.old_file_data)

    def insert_last_comma(self):
        for i in range(len(self.old_file_data)):
            self.old_file_data[i] += ';'

    def start_collumn_dict(self):
        column_dict = {}
        column_dict['Year'] = []

        for i in self.keylist:
            column_dict[i] = []
        return column_dict

    def set_collumns(self):
        for i in range(len(self.old_file_data)):
            #print(self.old_file_data)
            #print(self.column_dict)
            cont = 0
            fim = 0
            inicio = 0
            line = self.old_file_data[i]
            for j in range(len(line)):
                letter = line[j]
                fim += 1
                if letter == ";":
                    word = line[inicio:fim-1]
                    #print(i, word)
                    if cont == 0:
                        self.column_dict['Year'].append(int(word))
                    elif cont < 13:
                        #print(cont, self.keylist[cont-1])
                        self.column_dict[self.keylist[cont-1]].append(float(word))
                    cont += 1
                    inicio = fim
        #self.printColumnDict()

    def print_column_dict(self):
        for key in self.column_dict:
            print(key, len(self.column_dict[key]), self.column_dict[key])
        print('\n')

    def set_data_frame(self):
        self.data_frame = pd.DataFrame({key : self.column_dict[key] for key in self.keylist},
                                       index=self.column_dict['Year'])
        #self.dataFrame = self.dataFrame[self.dataFrame.index != '']
        #self.dataFrame =self.dataFrame.replace(['', ' '], [np.nan, np.nan])
        self.data_frame.index.name = 'Year'
        #print(self.dataFrame)

    def set_csv(self, sep_list, name):
        #print(self.old_file_data)
        self.replace_separator(sep_list)
        #print(self.old_file_data)
        self.insert_last_comma()
        self.set_collumns()
        self.set_data_frame()
        self.save_csv(name)
        #print(self.column_dict)

    def save_csv(self, name):
        newpath = '../../data/files/original/csv/' + name + '.csv'
        with open(newpath, 'w') as file:
            self.data_frame.round(2).to_csv(file)


# -*- coding: utf-8 -*-
'''
Created on 2 de mai de 2016

@author: Nicoli Araujo
'''

class Rainfall2008_2015(FromTxtToCSV):
    '''
    Vem diretamente do chuvaMensal2008-2015.txt original. 
    Gera um arquivo:
        Year    rainfall_month
        1970   29.5
    2-10-1970   18.2
    3-10-1970   7
    4-10-1970   0
    5-10-1970   3.9
    6-10-1970   0
    
    para cada mês.
    
    Não descarta os nans.
    

    '''
    def set_collumns(self):
        '''cria listas com os dados retirados do arquivo de entrada para ser manipulados posteriormente'''
        for line in self.old_file_data:
            cont = 0
            fim = 0
            inicio = 0
            for i in line:
                fim +=1
                if (i==";"):
                    cont+=1
                    if (cont == 2):
                        self.col_date.append(line[inicio:fim-1]) 
                    elif (cont == 4):
                        self.col_rainfall.append(line[inicio:fim-1])
                    inicio = fim
        #print(self.col_date, self.col_rainfall)
    def set_data_frame(self):
        self.data_frame = pd.DataFrame( {self.labelList[0]: self.col_rainfall}, 
                                        index = pd.to_datetime(self.col_date))
        self.data_frame =self.data_frame.replace(['', ' '], [np.nan, np.nan])
        self.data_frame.index.name = 'Date'
        print(self.data_frame)
    def set_months_data_frame(self):
        #print(self.data_frame)
        indexlist = [i for i in range(2008, 2016)]
        for key in self.keylist:
            df_month = self.data_frame.loc[self.data_frame.index.month == int(key)]
            df_month.rename(columns={'rainfall': key}, inplace=True)
            df_month.index = indexlist
            self.months_data_frame = pd.concat([self.months_data_frame, df_month], axis=1)
            #print(self.months_data_frame)
    
    
    def set_data(self, path):
        '''
        pega os dados localizados em path, padroniza e os transfere para um dataFrame
        '''
        self.old_file_data = self.get_old_file_data(path)
        self.remove_first_lines(17)
        self.set_collumns()
        self.set_data_frame()


    def __init__(self, filepath):
        '''
        Constructor
        '''
        '''name  =  txt name'''
        self.keylist = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.labelList = ['rainfall']
        #self.labelList = ['']
        self.col_date = []
        self.col_rainfall = []
        self.set_data(filepath)
        self.months_data_frame = pd.DataFrame({}, index = [i for i in range(2008,2015)])

        #print(self.months_data_frame)
