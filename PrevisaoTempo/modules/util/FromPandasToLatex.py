'''
Created on 29 de dez de 2016

@author: nicoli
'''
import pandas as pd


class ToLatex():
    def __init__(self, path_input=''):
        self.path_input = path_input
        # self.path_output = path_output
        self.pandas_data_set = pd.DataFrame
        self.latex_table = ''
        
    def read_data_set(self):
        return pd.read_csv(self.path_input, sep=r',', index_col=0).round(5)
    
    def from_csv_to_latex(self):
        self.pandas_data_set = self.read_data_set()

        self.pandas_data_set = pd.DataFrame(self.pandas_data_set.mean().round(2))
         
        self.pandas_data_set = self.pandas_data_set.transpose()
        for column in self.pandas_data_set.columns:
            if column[:-3] != 'rainfall':
                self.pandas_data_set.drop(column, axis=1, inplace=True)
         
         
        self.pandas_data_set.rename(columns={col:col.replace('rainfall_', '') for col in self.pandas_data_set.columns}, inplace=True)
        self.pandas_data_set.rename(columns={col:int(col) for col in self.pandas_data_set.columns}, inplace=True)
        print(self.pandas_data_set)
        self.latex_table = self.pandas_data_set.to_latex()
        
            
    def save_latex(self, filename):
        with open(filename, 'w') as file:
            file.write(self.latex_table)

def set_dict_nome_variaveis(df):
    dict = {'rainfall': 'Precipitação ',
            'nino12': 'Niño 1.2 ',
            'nino3': 'Niño 3 ',
            'nino34': 'Niño 3.4 ',
            'nino4': 'Niño 4 ',
            'tsa': 'TSA '}
    
    # col_list = [col for col in df.columns if (col[:-3] == 'rainfall_')]
    print(df.columns)
    df.rename(columns={oldname: dict[oldname[:-3]] + oldname[-2:] for oldname in df.columns}, inplace=True)
    a = str(df.index[0])
    df.index = [dict[a[:-3]] + a[-2:]]
    return df
def save_dataset(dataset, filename):
    dataset = set_dict_nome_variaveis(dataset.transpose())
    latex = dataset.transpose().to_latex()
    print(latex)
    with open(filename, 'w') as file:
        file.write(latex)
        
if __name__ == '__main__':
    # print('oier')
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    # ETC = '_regression_dataset_normalized'
    ETC = '_inputs'
    # PATH_INPUT = '../../data/files/ann_output_files/' + MONTH + '_' + TIME_GAP  + ETC + '.csv'
    PATH_INPUT = '../../data/files/original/AllData.csv'
    # PATH_INPUT = '../../data/files/ann_output_files/01_6_regression_dataset_normalized.csv'
    # PATH_INPUT = '../../data/files/anninputs/nonnormalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    # PATH_OUTPUT = '../../data/files/latex/' + 'tabela' + MONTH + '_' + TIME_GAP + ETC + '.tex'
    # PATH_OUTPUT = '../../data/files/latex/' + 'tabela' + MONTH + '_' + TIME_GAP + ETC + '.tex'
    jan = ToLatex(PATH_INPUT)
    jan.from_csv_to_latex()
    print(jan.latex_table)
    # jan.save_latex(PATH_OUTPUT)
    
    
