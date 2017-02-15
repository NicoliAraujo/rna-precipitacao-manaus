'''
Created on 17 de fev de 2017

@author: nicoli
'''

import pandas as pd
import seaborn as sns

class ANNPredictPlotting():
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(5)
    
    def plotanomaly(self):
        
        self.g = sns.factorplot(x='Year', y='Anomaly', hue = 'from', data=self.dataset, size = 8, aspect = 3,
                   kind="bar", palette="muted")
        self.g.despine(left=True)
        self.g.set_ylabels("survival probability")
        sns.plt.savefig('../../data/images/anomalydata/' + '01' + 'normalized' + '.png')
    
    def __init__(self, filename):
        self.dataset = self.read_data_set(filename)
        self.plotanomaly()
        #self.g.show()
if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    FILENAME = '../../data/files/ann_output_files/predict_comp' + MONTH + '_' + TIME_GAP + '_regression_normalized.csv'
    
    PLOT = ANNPredictPlotting(FILENAME)
    