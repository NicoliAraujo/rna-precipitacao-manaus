'''
Created on 5 de abr de 2017

@author: pibic-elloa-nicoli
'''
from modules.df_statistics.DataStatistics import Correlacao
if __name__ == '__main__':
    c = Correlacao('AllNormalizedData')
    #Colocar o mês pra correlação
    mes = '05'
    c.get_corr_dataset(mes)
    c.save_df_to_csv(mes)