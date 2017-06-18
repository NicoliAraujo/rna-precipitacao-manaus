'''
Created on 17 de jun de 2017

@author: nicoli
'''
import pandas as pd
def read_data_set(filename):
    '''abrir arquivos'''
    return pd.read_csv(filename, sep=r',', index_col=0)

if __name__ == '__main__':
    FILENAME = '../../data/files/original/csv/AllData.csv'
    df_all_data = read_data_set(FILENAME)
    df_mean_rf = pd.DataFrame({'Mês':[], 'Média': [], 'Mediana': [], 'Desvio Padrão':[]})
    for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        df_mean_rf = df_mean_rf.append({'Mês':i, 'Média': df_all_data['rainfall_'+ i].mean(), 'Mediana': df_all_data['rainfall_'+i].median(), 'Mediana': df_all_data['rainfall_'+i].median(), 'Desvio Padrão': df_all_data['rainfall_'+i].std()}, ignore_index=True)
    df_mean_rf = df_mean_rf[['Mês', 'Média', 'Mediana', 'Desvio Padrão']]
    
    print(df_mean_rf.round(1).T.to_latex())