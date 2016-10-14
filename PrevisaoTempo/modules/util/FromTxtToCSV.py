# -*- coding: utf-8 -*-
'''
Created on 12 de set de 2016

@author: Nicoli Araujo
'''
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
        newpath = '../data/original/csv/' + name + '.csv'
        with open(newpath, 'w') as file:
            self.data_frame.round(2).to_csv(file)

if __name__ == '__main__':
    PATH = '../data/original/other/rainfall.txt'
    MANAUS_MENSAL = MMFromTxtToCSV(PATH)
    MANAUS_MENSAL.set_csv(['\t'], 'rainfall')

    PATH = '../data/original/other/nino1+2.txt'
    NINO12 = MMFromTxtToCSV(PATH)
    NINO12.set_csv(['  '], 'nino12')

    PATH = '../data/original/other/nino3.txt'
    NINO3 = MMFromTxtToCSV(PATH)
    NINO3.set_csv(['  '], 'nino3')

    PATH = '../data/original/other/nino34.txt'
    NINO34 = MMFromTxtToCSV(PATH)
    NINO34.set_csv(['  '], 'nino34')

    PATH = '../data/original/other/nino4.txt'
    NINO4 = MMFromTxtToCSV(PATH)
    NINO4.set_csv(['  '], 'nino4')

    PATH = '../data/original/other/tsa.txt'
    TSA = MMFromTxtToCSV(PATH)
    TSA.set_csv(['    ', '   '], 'tsa')
