'''
Created on 17 de fev de 2017

@author: nicoli
'''

import pandas as pd
import seaborn as sns

class ANNPredictPlotting():
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(5)
    
    def plotanomaly(self, type):
        
        self.g = sns.factorplot(x='Year', y='Norm', hue = 'from', data=self.dataset, size = 8, aspect = 3,
                   kind="bar", palette="muted")
        self.g.despine(left=True)
        self.g.set_ylabels("Results")
        sns.plt.savefig('../../data/images/predictanalysis/' + '01' + type + '.png')
    
    def __init__(self, filename, type):
        self.dataset = self.read_data_set(filename)
        self.plotanomaly(type)
        #self.g.show()
if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    TYPE1 = 'regression_normalized'
    TYPE2 = 'regression_volume'
    TYPE3 = 'regression_volume'
    FILENAME_NORM = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE1 + '_seaborn.csv'
    FILENAME_VOLUME = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE2 +'_seaborn.csv'
    FILENAME_ANOMALY = '../../data/files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE3 +'_seaborn.csv'
    PLOT = ANNPredictPlotting(FILENAME_NORM, TYPE1)
    PLOT = ANNPredictPlotting(FILENAME_VOLUME, TYPE2)
    