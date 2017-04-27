'''
Created on 5 de abr de 2017

@author: pibic-elloa-nicoli
'''
from modules.df_statistics.DataStatistics import Correlacao
from modules.util.FromPandasToLatex import save_dataset as save

if __name__ == '__main__':
    c = Correlacao('AllNormalizedData')
    #Colocar o mês pra correlação
    mes = '01'
    atributo_alvo = 'rainfall'
    janela=6

    c.set_corr_dataset(atributo_alvo, mes, 6, op=1)
    nome='atributos_'+mes+'rainfall'
    save(c.corr_dataset, '../../data/files/latex/correlacao/'+nome+'.tex')

    c.set_corr_dataset(atributo_alvo,mes, 6, op=2)
    nome='atributos_'+mes
    save(c.corr_dataset, '../../data/files/latex/correlacao/'+nome+'.tex')

    c.set_corr_dataset(atributo_alvo,mes, 6, op=3)
    nome='atributos_defasados_'+mes
    save(c.corr_dataset, '../../data/files/latex/correlacao/'+nome+'.tex')

    #c.save_df_to_csv(mes)
    