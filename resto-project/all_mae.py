import pandas as pd
import numpy as np
#######IMPORT THE CSV WITH ALL THE FEATURES AND y_true AND y_pred
X_mae_d2 = pd.read_csv('../raw_data/features_mae_d2.csv')
X_mae_d16 = pd.read_csv('../raw_data/features_mae_d16.csv')
index_di = ['Daroco Bourse','Daroco 16']
CA_d2 = pd.read_csv('../raw_data/CA_d2.csv')
CA_d16 = pd.read_csv('../raw_data/CA_d16.csv')


def daily_maes():
    prov_dict_d2 = {}
    prov_dict_d16 = {}
    for i in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
        daily_series_d2 = X_mae_d2[X_mae_d2['jour']==i]
        daily_series_d16 = X_mae_d16[X_mae_d16['jour']==i]

        daily_mae_d2 = np.abs(daily_series_d2['y_true']-daily_series_d2['y_pred'])
        daily_mae_d16 = np.abs(daily_series_d16['y_true']-daily_series_d16['y_pred'])

        prov_dict_d2[i]=daily_mae_d2.mean()
        prov_dict_d2[f'{i} % total']=prov_dict_d2[i]/CA_d2[i].mean()

        prov_dict_d16[i]=daily_mae_d16.mean()
        prov_dict_d16[f'{i} % total']=prov_dict_d16[i]/CA_d16[i].mean()
    daily_maes_d2 = pd.DataFrame(data=prov_dict_d2, index=index_di)
    daily_maes_d16 = pd.DataFrame(data=prov_dict_d16, index=index_di)
    daily_maes = pd.concat([daily_maes_d2, daily_maes_d16]).drop_duplicates()
    print(daily_maes)
    daily_maes.to_csv('../raw_data/daily_maes.csv')


def service_maes():
    prov_dict_d2 = {}
    prov_dict_d16 = {}
    for i in ['soir','midi']:
        service_series_d2 = X_mae_d2[X_mae_d2['service']==i]
        service_series_d16 = X_mae_d16[X_mae_d16['service']==i]

        service_mae_d2 = np.abs(service_series_d2['y_true']-service_series_d2['y_pred'])
        service_mae_d16 = np.abs(service_series_d16['y_true']-service_series_d16['y_pred'])

        prov_dict_d2[i]=service_mae_d2.mean()
        prov_dict_d2[f'{i} % total']=prov_dict_d2[i]/CA_d2[i].mean()
        prov_dict_d16[i]=service_mae_d16.mean()
        prov_dict_d16[f'{i} % total']=prov_dict_d16[i]/CA_d16[i].mean()

    service_maes_d2 = pd.DataFrame(data=prov_dict_d2, index=index_di)
    service_maes_d16 = pd.DataFrame(data=prov_dict_d16, index=index_di)
    service_maes = pd.concat([service_maes_d2, service_maes_d16]).drop_duplicates()
    print(service_maes)
    service_maes.to_csv('../raw_data/service_maes.csv')

def daily_service_maes():
    prov_dict_d2 = {}
    prov_dict_d16 = {}
    for y in ['soir','midi']:
        for i in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
            concat = f'{i} {y}'
            daily_service_series_d2 = X_mae_d2[(X_mae_d2['jour']==i) & (X_mae_d2['service']==y)]
            daily_service_series_d16 = X_mae_d16[(X_mae_d16['jour']==i) & (X_mae_d16['service']==y)]

            daily_service_mae_d2 = np.abs(daily_service_series_d2['y_true']-daily_service_series_d2['y_pred'])
            daily_service_mae_d16 = np.abs(daily_service_series_d16['y_true']-daily_service_series_d16['y_pred'])

            prov_dict_d2[f'{i} {y}']=daily_service_mae_d2.mean()
            prov_dict_d2[f'{i} {y} % total'] = prov_dict_d2[concat]/CA_d2[concat].mean()
            prov_dict_d16[f'{i} {y}']=daily_service_mae_d16.mean()
            prov_dict_d16[f'{i} {y} % total'] = prov_dict_d16[concat]/CA_d16[concat].mean()

    daily_service_maes_d2 = pd.DataFrame(data=prov_dict_d2, index=index_di)
    daily_service_maes_d16 = pd.DataFrame(data=prov_dict_d16, index=index_di)
    daily_service_maes = pd.concat([daily_service_maes_d2,daily_service_maes_d16]).drop_duplicates()
    daily_service_maes.to_csv('../raw_data/daily_service_maes.csv')

if __name__ == '__main__':
    daily_maes()
    service_maes()
    daily_service_maes()
