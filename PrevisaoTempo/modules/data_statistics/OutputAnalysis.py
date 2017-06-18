'''
Created on 17 de jun de 2017

@author: nicoli
'''
import pandas as pd
def read_data_set(filename):
    '''abrir arquivos'''
    return pd.read_csv(filename, sep=r',', index_col=0)

ARQ_DICT = {'(4, 8)': [37, 4, 8, 1], '9': [37, 9, 1], '(7, 5)': [37, 7, 5, 1], '(5, 7)': [37, 5, 7, 1], '(8, 4)': [37, 8, 4, 1], '3': [37, 3, 1], '6': [37, 6, 1], '7': [37, 7, 1], '11': [37, 11, 1], '10': [37, 10, 1], '12': [37, 12, 1], '(9, 3)': [37, 9, 3, 1], '(6, 6)': [37, 6, 6, 1], '4': [37, 4, 1], '(3, 9)': [37, 3, 9, 1], '5': [37, 5, 1], '8': [37, 8, 1]}


def set_arq(df):
    arq_list = list(df['Arquitetura'])
    for i in range(len(arq_list)):
        arq_list[i] = ARQ_DICT[arq_list[i]]
    df['Arquitetura'] = arq_list
if __name__ == '__main__':
    results_df = pd.DataFrame()
    for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        MONTH = i
        TIME_GAP = '6'
        FILENAME = '../../data/files/ann_output_files/scale/'+ MONTH + '_' + TIME_GAP + '_scale.csv'
        month_df = read_data_set(FILENAME)
        month_df['Mês'] = int(i)
        #print(month_df['Arquitetura'].head(5))
        results_df = results_df.append(month_df.head(1))
        
    set_arq(results_df)
    results_df.loc[results_df['FA']=='tanh', 'FA'] = 'Tangente Hiperbólica'
    results_df.loc[results_df['FA']=='logistic', 'FA'] = 'Sigmoidal'
    results_df['Acurácia'] = results_df['ACURACIA'].round(2)
    results_df.drop('ACURACIA', 1, inplace = True)
    results_df.drop('FV', 1, inplace = True)
    
    #results_df.index = [i for i in range(1, len(results_df)+1)]
    results_df = results_df[['Mês', 'Arquitetura', 'FA', 'Alpha', 'TA', 'Acurácia']]
    print(results_df.to_latex())