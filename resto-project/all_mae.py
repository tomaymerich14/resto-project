import pandas as pd
import numpy as np
#######IMPORT THE CSV WITH ALL THE FEATURES AND y_true AND y_pred
X_mae_d2 = pd.read_csv('../raw_data/features_mae_d2.csv')
#X_mae_d16 = pd.read_csv('../raw_data/features_mae_d16.csv')

def daily_maes():
    prov_dict = {}
    for i in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
        daily_series = X_mae_d2[X_mae_d2['jour']==i]
        daily_mae = np.abs(daily_series['y_true']-daily_series['y_pred'])
        prov_dict[i]=daily_mae.mean()
    daily_maes = pd.DataFrame(data=prov_dict, index=[0])
    print(daily_maes)
    daily_maes.to_csv('../raw_data/daily_maes.csv')

def service_maes():
    prov_dict = {}
    for i in ['soir','midi']:
        service_series = X_mae_d2[X_mae_d2['service']==i]
        service_mae = np.abs(service_series['y_true']-service_series['y_pred'])
        prov_dict[i]=service_mae.mean()
    service_maes = pd.DataFrame(data=prov_dict, index=[0])
    print(service_maes)
    service_maes.to_csv('../raw_data/service_maes.csv')

def daily_service_maes():
    prov_dict = {}
    for y in ['soir','midi']:
        for i in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
            daily_service_series = X_mae_d2[(X_mae_d2['jour']==i) & (X_mae_d2['service']==y)]
            daily_service_mae = np.abs(daily_service_series['y_true']-daily_service_series['y_pred'])
            prov_dict[f'{i} {y}']=daily_service_mae.mean()
    daily_service_maes = pd.DataFrame(data=prov_dict, index=[0])
    daily_service_maes.to_csv('../raw_data/daily_service_maes.csv')

if __name__ == '__main__':
    daily_maes()
    service_maes()
    daily_service_maes()
