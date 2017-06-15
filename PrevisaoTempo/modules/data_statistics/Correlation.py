'''
Created on 3 de mai de 2017

@author: pibic-elloa-nicoli
'''
from modules.util.FromPandasToLatex import save_dataset as save
import pandas as pd


class Correlation():
    '''Classe que tira a correlação entre vários membros do dataset 
    '''
    def get_normalized_data(self):
        filepath = '../../data/files/original/csv/' + self.name + '.csv'
        return pd.read_csv(filepath, sep=r',', index_col='Year')
    
    def set_corr_dataset(self, attribute, month, time_gap, op):
        target = attribute + '_' + month
        # col_list = self.get_col_list(month)
        self.corr_dataset = self.get_dataset(month, time_gap, op)
        # print(self.corr_dataset.columns)
        self.corr_dataset = pd.DataFrame(self.corr_dataset.corr()['rainfall_' + month]).transpose()
        self.corr_dataset.index = [target]
        self.corr_dataset = self.corr_dataset.transpose().round(3)
        
        print(self.corr_dataset)
    
    # def get_dataset(self, name_list, target):
    def set_relacao_corr(self, dataset, target):
        '''edita um dataset para ver se a correlação é positiva, negativa ou neutra'''
        self.corr_dataset['Relacao'] = 'Neutra'
        print(self.corr_dataset.loc[self.corr_dataset['Valor'] > 0]['Relacao'])
        # print(self.corr_dataset.loc[:,'rainfall_01'])
        self.corr_dataset.loc[self.corr_dataset[target] > 0, 'Relacao'] = 'Positiva'
        self.corr_dataset.loc[self.corr_dataset[target] < 0, 'Relacao'] = 'Negativa'
        
    def get_dataset(self, month, time_gap, op):
        '''dá um dataset para apenas um atributo, ex: rainfall. Apenas esse atributo será avaliado em todos os meses
        op==1: 'todos os rainfall, demais atributos são do mês escolhido'
        op==2: 'todos os atributos do mês escolhido'
        op==3: 'atributos defasados'''
        
        if op == 1:
            col_list = [col for col in self.df.columns if (col[:-2] == 'rainfall_' or col[-2:] == month)]
        elif op == 2:
            col_list = [col for col in self.df.columns if (col[-2:] == month)] 
        elif op == 3:
            all_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            month_list = [all_months[int(month) - i] for i in range(2, time_gap + 2)]
            month_list.append(month)
            col_list = [col for col in self.df.columns if (col[-2:] in month_list)]
        # print('col_list: ',col_list)
        return self.df[col_list]
    
    def save_df_to_csv(self, info):
        filename = '../../data/files/statistics/' + info + '_Correlacao.csv'
        with open(filename, 'w') as file:
            self.corr_dataset.to_csv(file)
    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.df = self.get_normalized_data()
        


if __name__ == '__main__':
    c = Correlation('AllNormalizedData')
    # Colocar o mês pra correlação
    mes = '01'
    atributo_alvo = 'rainfall'
    janela = 6

    c.set_corr_dataset(atributo_alvo, mes, 6, op=1)
    nome = 'atributos_' + mes + 'rainfall'
    save(c.corr_dataset, '../../data/files/latex/correlacao/' + nome + '.tex')

    c.set_corr_dataset(atributo_alvo, mes, 6, op=2)
    nome = 'atributos_' + mes
    save(c.corr_dataset, '../../data/files/latex/correlacao/' + nome + '.tex')

    c.set_corr_dataset(atributo_alvo, mes, 6, op=3)
    nome = 'atributos_defasados_' + mes
    save(c.corr_dataset, '../../data/files/latex/correlacao/' + nome + '.tex')

    # c.save_df_to_csv(mes)
