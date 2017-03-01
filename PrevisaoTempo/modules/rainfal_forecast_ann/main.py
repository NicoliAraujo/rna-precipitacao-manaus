'''
Created on 26 de fev de 2017

@author: nicoli
'''
from Regressor import RainfallRegressor

from PredictBest import Predict_Best

if __name__ == '__main__':
    MONTH = '01'
    TIME_GAP = '6'
    EXTENSION = 'csv'
    FILENAME = '../../data/files/anninputs/normalizedinputs/' + MONTH+ '_' + TIME_GAP + '.' + EXTENSION
    RFANN = RainfallRegressor(FILENAME, n_layers=2, n_nodes=7)
    RFANN.fit_networks()
    RFANN.predict_networks()
    RFANN.save_networks(MONTH, TIME_GAP)
    
    RESULT_NETS_CSV = '../../data/files/ann_output_files/' + MONTH+ '_' + TIME_GAP + '_regression_dataset_normalized.csv'
    
    PB = Predict_Best(RFANN.result_networks, RFANN.test_data, MONTH, num_nets=5)
    PB.set_predict_df()
    PB.set_predict_df_seaborn()
 
    FILENAME_NORM_ANOMALY_VIEW = '../../data/files/ann_output_files/ann_output_view/' + MONTH + '_' + TIME_GAP + '_regression_normalized_anomaly.csv'
    FILENAME_NORM_ANOMALY_SEABORN = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_normalized_anomaly_seaborn.csv'
     
    FILENAME_PREDICT = '../../data/files/ann_output_files/ann_output_view/' + MONTH + '_' + TIME_GAP + '_regression_normalized.csv'
    FILENAME_PREDICT_SEABORN = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_normalized_seaborn.csv'
     
    PB.save_predict_df_seaborn(FILENAME_PREDICT_SEABORN, FILENAME_NORM_ANOMALY_SEABORN)
    PB.save_predict_df(FILENAME_PREDICT, FILENAME_NORM_ANOMALY_VIEW)
     
    FILENAME_VOLUME_SEABORN = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_volume_seaborn.csv'
    FILENAME_VOLUME = '../../data/files/ann_output_files/ann_output_view/' + MONTH + '_' + TIME_GAP + '_regression_volume.csv'
 
    FILENAME_SOURCE = '../../data/files/original/AllData.csv'
     
    FILENAME_VOLUME_ANOMALY_VIEW = '../../data/files/ann_output_files/ann_output_view/' + MONTH + '_' + TIME_GAP + '_regression_volume_anomaly.csv'
    FILENAME_VOLUME_ANOMALY_SEABORN = '../../data/files/ann_output_files/ann_output_seaborn/' + MONTH + '_' + TIME_GAP + '_regression_volume_anomaly_seaborn.csv'
     
    PB.start_predict_dfs_volume(FILENAME_SOURCE)
    PB.save_predict_df_volume(FILENAME_VOLUME_SEABORN, FILENAME_VOLUME, 
                              FILENAME_VOLUME_ANOMALY_SEABORN, FILENAME_VOLUME_ANOMALY_VIEW)
     