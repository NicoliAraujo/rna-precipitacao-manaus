'''
Created on 26 de fev de 2017

@author: nicoli
'''
# from modules.rainfal_forecast_ann.Regressor import R

from modules.rainfal_forecast_ann.RainfallRegressor import RainfallRegressor
from modules.rainfal_forecast_ann.ResultsParser import ResultsParser


if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    ETC = '18pcs'
    FILENAME = '../../data/files/anninputs/pca_inputs/' + MONTH + '_' + TIME_GAP + '_' + ETC + '.' + EXTENSION
    
    FILENAME_NORM_ANOMALY_VIEW = ['../../data/files/ann_output_files/ann_output_view/', MONTH + '_' + TIME_GAP + '_regression_normalized_anomaly.csv']
    FILENAME_NORM_ANOMALY_SEABORN = ['../../data/files/ann_output_files/ann_output_seaborn/', MONTH + '_' + TIME_GAP + '_regression_normalized_anomaly_seaborn.csv']
    
    FILENAME_PREDICT = ['../../data/files/ann_output_files/ann_output_view/' , MONTH + '_' + TIME_GAP + '_regression_normalized.csv']
    FILENAME_PREDICT_SEABORN = ['../../data/files/ann_output_files/ann_output_seaborn/', MONTH + '_' + TIME_GAP + '_regression_normalized_seaborn.csv']
    
    FILENAME_VOLUME_SEABORN = ['../../data/files/ann_output_files/ann_output_seaborn/', MONTH + '_' + TIME_GAP + '_regression_volume_seaborn.csv']
    FILENAME_VOLUME = ['../../data/files/ann_output_files/ann_output_view/', MONTH + '_' + TIME_GAP + '_regression_volume.csv']
 
    FILENAME_SOURCE = '../../data/files/original/csv/AllData.csv'
     
    FILENAME_VOLUME_ANOMALY_VIEW = ['../../data/files/ann_output_files/ann_output_view/', MONTH + '_' + TIME_GAP + '_regression_volume_anomaly.csv']
    FILENAME_VOLUME_ANOMALY_SEABORN = ['../../data/files/ann_output_files/ann_output_seaborn/', MONTH + '_' + TIME_GAP + '_regression_volume_anomaly_seaborn.csv']
     
    RESULT_NETS_CSV = ['../../data/files/ann_output_files/', MONTH + '_' + TIME_GAP + '_regression_dataset_normalized.csv']
    
    
    RFANN = RainfallRegressor(FILENAME, n_layers=2, n_nodes=7)
    RFANN.fit_networks()
    RFANN.predict_networks()
    RFANN.save_networks(MONTH, TIME_GAP)
    
    PS = ResultsParser(RFANN.result_networks, RFANN.test_data, MONTH, num_nets=3, source_df_filename=FILENAME_SOURCE)
    PS.set_results_dfs()
    PS.set_parser_results_seaborn()
 
    PS.save_results_dfs(filename_norm_results_view=FILENAME_PREDICT,
                        filename_norm_results_anomaly_view=FILENAME_NORM_ANOMALY_VIEW,
                        filename_results_df_volume_view=FILENAME_VOLUME,
                        filename_results_anomaly_volume_view=FILENAME_VOLUME_ANOMALY_VIEW)
    
    PS.save_seaborn_dfs(filename_results_df_volume_seaborn=FILENAME_VOLUME_SEABORN,
                        filename_anomaly_volume_seaborn=FILENAME_VOLUME_ANOMALY_SEABORN,
                        filename_results_norm_seaborn=FILENAME_PREDICT_SEABORN,
                        filename_norm_anomaly_seaborn=FILENAME_NORM_ANOMALY_SEABORN)
    
    
