import numpy as np
import pandas as pd

def cyclical_columns():
    for i in [2,16]:
        forecast_set = f'../raw_data/forecasted_services_d{i}.csv'

        forecast_set_all = pd.read_csv(forecast_set)

            # ----------------Create cyclical columns ----------------

        forecast_set_all['jour_de_sem_norm'] = 2* np.pi * forecast_set_all['jour_de_sem'] / max(forecast_set_all['jour_de_sem'])
        forecast_set_all['cos_jour_de_sem'] = np.cos(forecast_set_all['jour_de_sem_norm'])
        forecast_set_all['sin_jour_de_sem'] = np.sin(forecast_set_all['jour_de_sem_norm'])


        forecast_set_all['jour_du_mois_norm'] = 2* np.pi * forecast_set_all['jour_du_mois'] / max(forecast_set_all['jour_du_mois'])
        forecast_set_all['cos_jour_du_mois'] = np.cos(forecast_set_all['jour_du_mois_norm'])
        forecast_set_all['sin_jour_du_mois'] = np.sin(forecast_set_all['jour_du_mois_norm'])


        forecast_set_all['mois_de_annee_norm'] = 2* np.pi * forecast_set_all['mois_de_annee'] / max(forecast_set_all['mois_de_annee'])
        forecast_set_all['cos_mois_de_annee'] = np.cos(forecast_set_all['mois_de_annee_norm'])
        forecast_set_all['sin_mois_de_annee'] = np.sin(forecast_set_all['mois_de_annee_norm'])


        forecast_set_all['jour_annee_norm'] = 2* np.pi * forecast_set_all['jour_annee'] / max(forecast_set_all['jour_annee'])
        forecast_set_all['cos_jour_annee'] = np.cos(forecast_set_all['jour_annee_norm'])
        forecast_set_all['sin_jour_annee'] = np.sin(forecast_set_all['jour_annee_norm'])


        forecast_set_all['semaine_annee_norm'] = 2* np.pi * forecast_set_all['sem_de_annee'] / max(forecast_set_all['sem_de_annee'])
        forecast_set_all['cos_semaine_annee'] = np.cos(forecast_set_all['semaine_annee_norm'])
        forecast_set_all['sin_semaine_annee'] = np.sin(forecast_set_all['semaine_annee_norm'])


        forecast_set_all.drop(columns=['semaine_annee_norm','jour_annee_norm','mois_de_annee_norm','jour_du_mois_norm','jour_de_sem_norm','jour_de_sem','jour_du_mois','mois_de_annee','sem_de_annee','jour_annee','Unnamed: 0'], inplace=True)

        forecast_set_all.to_csv(f'../raw_data/forecasted_services_d{i}.csv',index=False)

        pass

if __name__ == '__main__':
    cyclical_columns()
