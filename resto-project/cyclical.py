import numpy as np
import pandas as pd

def cyclical_columns():

    dataset_d16 = '../raw_data/preproc_data_d16.csv'
    dataset_d2 = '../raw_data/preproc_data_d2.csv'

    data_d16 = pd.read_csv(dataset_d16)
    data_d2 = pd.read_csv(dataset_d2)
        # ----------------Create cyclical columns ----------------
    data_d16['jour_de_sem_norm'] = 2* np.pi * data_d16['jour_de_sem'] / max(data_d16['jour_de_sem'])
    data_d16['cos_jour_de_sem'] = np.cos(data_d16['jour_de_sem_norm'])
    data_d16['sin_jour_de_sem'] = np.sin(data_d16['jour_de_sem_norm'])

    data_d2['jour_de_sem_norm'] = 2* np.pi * data_d2['jour_de_sem'] / max(data_d2['jour_de_sem'])
    data_d2['cos_jour_de_sem'] = np.cos(data_d2['jour_de_sem_norm'])
    data_d2['sin_jour_de_sem'] = np.sin(data_d2['jour_de_sem_norm'])

    data_d16['jour_du_mois_norm'] = 2* np.pi * data_d16['jour_du_mois'] / max(data_d16['jour_du_mois'])
    data_d16['cos_jour_du_mois'] = np.cos(data_d16['jour_du_mois_norm'])
    data_d16['sin_jour_du_mois'] = np.sin(data_d16['jour_du_mois_norm'])

    data_d2['jour_du_mois_norm'] = 2* np.pi * data_d2['jour_du_mois'] / max(data_d2['jour_du_mois'])
    data_d2['cos_jour_du_mois'] = np.cos(data_d2['jour_du_mois_norm'])
    data_d2['sin_jour_du_mois'] = np.sin(data_d2['jour_du_mois_norm'])

    data_d16['mois_de_annee_norm'] = 2* np.pi * data_d16['mois_de_annee'] / max(data_d16['mois_de_annee'])
    data_d16['cos_mois_de_annee'] = np.cos(data_d16['mois_de_annee_norm'])
    data_d16['sin_mois_de_annee'] = np.sin(data_d16['mois_de_annee_norm'])

    data_d2['mois_de_annee_norm'] = 2* np.pi * data_d2['mois_de_annee'] / max(data_d2['mois_de_annee'])
    data_d2['cos_mois_de_annee'] = np.cos(data_d2['mois_de_annee_norm'])
    data_d2['sin_mois_de_annee'] = np.sin(data_d2['mois_de_annee_norm'])

    data_d16['jour_annee_norm'] = 2* np.pi * data_d16['jour_annee'] / max(data_d16['jour_annee'])
    data_d16['cos_jour_annee'] = np.cos(data_d16['jour_annee_norm'])
    data_d16['sin_jour_annee'] = np.sin(data_d16['jour_annee_norm'])

    data_d2['jour_annee_norm'] = 2* np.pi * data_d2['jour_annee'] / max(data_d2['jour_annee'])
    data_d2['cos_jour_annee'] = np.cos(data_d2['jour_annee_norm'])
    data_d2['sin_jour_annee'] = np.sin(data_d2['jour_annee_norm'])

    data_d16['semaine_annee_norm'] = 2* np.pi * data_d16['sem_de_annee'] / max(data_d16['sem_de_annee'])
    data_d16['cos_semaine_annee'] = np.cos(data_d16['semaine_annee_norm'])
    data_d16['sin_semaine_annee'] = np.sin(data_d16['semaine_annee_norm'])

    data_d2['semaine_annee_norm'] = 2* np.pi * data_d2['sem_de_annee'] / max(data_d2['sem_de_annee'])
    data_d2['cos_semaine_annee'] = np.cos(data_d2['semaine_annee_norm'])
    data_d2['sin_semaine_annee'] = np.sin(data_d2['semaine_annee_norm'])

    data_d2.to_csv('../raw_data/preproc_data_d2.csv', index=False)
    data_d16.to_csv('../raw_data/preproc_data_d16.csv',index=False)

    data_d2.drop(columns=['semaine_annee_norm','jour_annee_norm','mois_de_annee_norm','jour_du_mois_norm','jour_de_sem_norm','jour_de_sem','jour_du_mois','mois_de_annee','sem_de_annee','jour_annee'])
    data_d16.drop(columns=['semaine_annee_norm','jour_annee_norm','mois_de_annee_norm','jour_du_mois_norm','jour_de_sem_norm','jour_de_sem','jour_du_mois','mois_de_annee','sem_de_annee','jour_annee'])
    pass

if __name__ == '__main__':
    cyclical_columns()
