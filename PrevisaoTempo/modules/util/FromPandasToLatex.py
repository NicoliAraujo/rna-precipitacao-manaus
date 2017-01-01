'''
Created on 29 de dez de 2016

@author: nicoli
'''
import pandas as pd
class ToLatex():
    def __init__(self, path_input):
        self.path_input = path_input
        #self.path_output = path_output
        self.pandas_data_set = pd.DataFrame
        self.latex_table = ''
        
    def read_data_set(self):
        return pd.read_csv(self.path_input, sep=r',', index_col=0).round(5)
    
    def from_csv_to_latex(self):
        self.pandas_data_set = self.read_data_set()
        self.latex_table = self.pandas_data_set.to_latex()
    
    def save_latex(self, filename):
        with open(filename, 'w') as file:
            file.write(self.latex_table)
if __name__ == '__main__':
    print('oier')
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    ETC = '_regression_dataset_normalized'
    PATH_INPUT = '../../data/files/ann_output_files/' + MONTH + '_' + TIME_GAP  + ETC + '.csv'
        
    #PATH_INPUT = '../../data/files/anninputs/normalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    PATH_OUTPUT = '../../data/files/latex/' + 'tabela' + MONTH + '_' + TIME_GAP + ETC + '.tex'
        
    jan = ToLatex(PATH_INPUT)
    jan.from_csv_to_latex()
    print(jan.latex_table)
    jan.save_latex(PATH_OUTPUT)