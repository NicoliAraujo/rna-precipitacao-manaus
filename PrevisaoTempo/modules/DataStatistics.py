'''
Created on 26 de set de 2016

@author: pibic-elloa-nicoli
'''
import pandas as pd


class Anomaly(object):
    '''
    classdocs
    '''
    def getOriginalData(self):
        return pd.read_csv('../data/original/csv/' + self.name + '.csv', sep = r',', index_col = 'Year' )
    
    def setAnomalyDF(self):
        self.anomalyDF = self.df - self.df.mean()
    
    def saveDFtoCSV(self):
        filename = '../data/files/anomalydata/' + self.name + '.csv'
        with open(filename, 'w') as file:
            self.anomalyDF.round(2).to_csv(file)
            
    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.df = self.getOriginalData()
        self.mean = 0
        self.anomalyDF = pd.DataFrame()
                
if __name__ == '__main__':
    anomalynino12 = Anomaly('nino12')
    anomalynino12.setAnomalyDF()
    anomalynino12.saveDFtoCSV()
    
    anomalynino3 = Anomaly('nino3')
    anomalynino3.setAnomalyDF()
    anomalynino3.saveDFtoCSV()
    
    anomalynino34 = Anomaly('nino34')
    anomalynino34.setAnomalyDF()
    anomalynino34.saveDFtoCSV()
    
    anomalymanaus_mensal = Anomaly('manaus_mensal')
    anomalymanaus_mensal.setAnomalyDF()
    anomalymanaus_mensal.saveDFtoCSV()
    
    anomalytsa = Anomaly('tsa')
    anomalytsa.setAnomalyDF()
    anomalytsa.saveDFtoCSV()
    
    anomalynino4 = Anomaly('nino4')
    anomalynino4.setAnomalyDF()
    anomalynino4.saveDFtoCSV()