'''
Created on 17 de fev de 2017

@author: nicoli
'''

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ResultNetsPlotting():
    def read_data_set(self, filename):
        return pd.read_csv(filename, sep=r',', index_col=0).round(5)
    
    def plotanomaly(self, type, dataset, month, time_gap):
#         #print(self.dataset)
        #col_list = ["black", "greenyellow", "aquamarine", 
        #            "hotpink", "gold", 'royalblue']
        col_list = ["mediumblue", "darkkhaki", "salmon", 
                    "palegreen", "paleturquoise", 'violet']
        #my_palette = [(sns.hls_palette(8, l=.3, s=.8)[5])]
        my_palette = ['black']
        print(my_palette)
        #print(my_palette)
        for color in sns.color_palette("colorblind", 7):
            my_palette.append(color)
        print(my_palette)
#         self.g = sns.factorplot(x='Year', y='Norm', hue = 'from', data=dataset, size = 8, aspect = 3,
#                    kind="bar", palette=col_list, legend=False)
#         
#         #self.g = sns.kdeplot(x='Year', y='Norm', data=self.dataset, palette='muted', hue='from')
#         self.g.despine(left=True)
#         self.g.set_ylabels("Precipitação")
#         self.g.set_xlabels("Ano")
#         plt.legend(loc='upper right')
#         sns.plotting_context("notebook", font_scale=8)
#         sns.plt.savefig('../../data/images/predictanalysis/' + '01' + type + '.png')
        with sns.plotting_context("notebook",font_scale=2):
            self.g = sns.factorplot(x='Year', y='Norm', hue = 'from', data=dataset, size = 12, aspect = 2,
                       kind="bar", palette=my_palette, legend=False)
            self.g.despine(left=True)
            sns.set_style("whitegrid")
            self.g.set_ylabels("Precipitação(mm)")
            self.g.set_xlabels("Ano")
            plt.legend(loc='upper right')
            self.g.set_titles(fontsize=2)
            sns.plt.savefig('../../data/images/predictanalysis/' + month + '_' + type + '_' + '.png')
            
    def __init__(self, filename, month, time_gap, type):
        '''self.dataset = self.read_data_set(filename)
        self.dataset1 = self.dataset[self.dataset['Year']>=2008]
        self.dataset2 = self.dataset[self.dataset['Year']<2008]
        #print(type)
        self.plotanomaly(type+'_pt1', self.dataset1, month, time_gap)
        self.plotanomaly(type+'_pt2', self.dataset2, month, time_gap,)'''
        self.dataset = self.read_data_set(filename)
        self.plotanomaly(type, self.dataset, month, time_gap)
        #self.g.show()
if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    #TYPE1 = 'regression_normalized'
    TYPE2 = 'regression_volume'
    TYPE3 = 'regression_volume_anomaly'
    #TYPE4 = 'regression_normalized_anomaly'
    
    #FILENAME_NORM = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE1 + '_seaborn.csv'
    FILENAME_VOLUME = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE2 +'_seaborn.csv'
    FILENAME_ANOMALY = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE3 +'_seaborn.csv'
    #FILENAME_NORM_ANOMALY = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_' + TYPE4 +'_seaborn.csv'
    
    #PLOT = ANNPredictPlotting(FILENAME_NORM, TYPE1)
    PLOT = ResultNetsPlotting(FILENAME_VOLUME, MONTH, TIME_GAP, TYPE2)
    PLOT = ResultNetsPlotting(FILENAME_ANOMALY, MONTH, TIME_GAP, TYPE3)
    #PLOT = ANNPredictPlotting(FILENAME_NORM_ANOMALY, TYPE4)
    
    
