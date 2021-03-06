'''
Created on 26 de fev de 2017

@author: nicoli
'''
# from modules.rainfal_forecast_ann.Regressor import R


from modules.rainfall_forecast_ann.Classifier import RainfallRegressorNets
from modules.rainfall_forecast_ann.ResultNetsViewVolume import ResultNetsView, ResultsParser
import pandas as pd


def read_data_set(filename):
        return pd.read_csv(filename, sep=r',', index_col=0)

if __name__ == '__main__':
    for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        MONTH = i
        TIME_GAP = '6'
        EXTENSION = 'csv'
        FILENAME = '../../data/files/anninputs/nonnormalizedinputs/' + MONTH + '_' + TIME_GAP + '.' + EXTENSION
        #FILENAME_NORM_ANOMALY_VIEW = ['../../data/files/ann_output_files/scale/ann_output_view/' + TIME_GAP +'/', MONTH + '_regression_stdscale_anomaly.csv']
        #FILENAME_NORM_ANOMALY_SEABORN = ['../../data/files/ann_output_files/scale/ann_output_seaborn/', MONTH + '_' + TIME_GAP + '_regression_stdscale_anomaly_seaborn.csv']
        
        #FILENAME_PREDICT = ['../../data/files/ann_output_files/scale/ann_output_view/'  + TIME_GAP +'/', MONTH + '_regression_stdscale.csv']
        #FILENAME_PREDICT_SEABORN = ['../../data/files/ann_output_files/scale/ann_output_seaborn/', MONTH + '_' + TIME_GAP + '_regression_stdscale_seaborn.csv']
        
        
         
        RESULT_NETS_CSV = ['../../data/files/ann_output_files/scale/' + TIME_GAP +'/', MONTH + '_'+ '_regression_dataset_stdscale.csv']
        
        # normalizando
        dataset_non_normalized = read_data_set(FILENAME)
        #print(dataset_non_normalized.mean())
        
        rfann = RainfallRegressorNets(dataset_non_normalized)
        rfann.train_test_nets()
        rfann.save_networks(MONTH, TIME_GAP)
        
        #PS = ResultsParser(rfann.neural_networks, rfann.test_data, MONTH, 5)
        
        #PS.set_results_dfs()
        #PS.set_seaborn_dfs()
     
        #PS.save_results_dfs(filename_norm_results_view=FILENAME_PREDICT,
        #                    filename_norm_results_anomaly_view=FILENAME_NORM_ANOMALY_VIEW)
                            
        
        #PS.save_seaborn_dfs(filename_results_norm_seaborn=FILENAME_PREDICT_SEABORN,
        #                    filename_norm_anomaly_seaborn=FILENAME_NORM_ANOMALY_SEABORN)
        print(i, ' terminado')