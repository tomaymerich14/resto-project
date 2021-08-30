import pandas as pd
import numpy as np
import datetime as dt
from numpy import mean
from numpy import std

#----------------------------------------

df_d2 = pd.read_csv('../raw_data/df_raw_d2.csv')
df_d16 =pd.read_csv('../raw_data/df_raw_d16.csv')

#------ D2 data date --------------------

df_d2['date'] = pd.to_datetime(df_d2['date'],  format='%Y-%m-%d')

df_d2['jour_de_sem'] = df_d2['date'].dt.weekday +1
df_d2['jour_du_mois'] = df_d2['date'].dt.day
df_d2['mois_de_annee'] = df_d2['date'].dt.month
df_d2['sem_de_annee'] = df_d2['date'].dt.week

def jour_annee(x):
    return x.toordinal() - dt.date(x.year, 1, 1).toordinal() + 1

df_d2['jour_annee'] = df_d2.apply(lambda x:jour_annee(x['date']), axis=1)

#------ D16 data date --------------------

df_d16['date'] = pd.to_datetime(df_d16['date'],  format='%Y-%m-%d')
df_d16['jour_de_sem'] = df_d16['date'].dt.weekday +1
df_d16['jour_du_mois'] = df_d16['date'].dt.day
df_d16['mois_de_annee'] = df_d16['date'].dt.month
df_d16['sem_de_annee'] = df_d16['date'].dt.week
df_d16['jour_annee'] = df_d16.apply(lambda x:jour_annee(x['date']), axis=1)

#------ D2 data financières --------------------

df_d2['moyen_7_services'] = 0
df_d2['moyen_31_services'] = 0

#Split
df_d2_midi = df_d2[df_d2['service']=='midi'].reset_index(drop=True)
df_d2_soir = df_d2[df_d2['service']=='soir'].reset_index(drop=True)

#For loops pour créer les colonnes
for i in range(df_d2_midi.shape[0]):
        if i >= 7:
            moy_service=[]
            for j in range(1,8):
                moy_service.append(df_d2_midi['CA_TTC'][i-j])
            df_d2_midi['moyen_7_services'][i]=mean(moy_service)
        else:
            df_d2_midi['moyen_7_services'][i]=np.nan

for i in range(df_d2_midi.shape[0]):
        if i >= 31:
            moy_mois=[]
            for j in range(1,32):
                moy_mois.append(df_d2_midi['CA_TTC'][i-j])
            df_d2_midi['moyen_31_services'][i]=mean(moy_mois)
        else:
            df_d2_midi['moyen_31_services'][i]=np.nan

for i in range(df_d2_soir.shape[0]):
        if i >= 7:
            moy_service=[]
            for j in range(1,8):
                moy_service.append(df_d2_soir['CA_TTC'][i-j])
            df_d2_soir['moyen_7_services'][i]=mean(moy_service)
        else:
            df_d2_soir['moyen_7_services'][i]=np.nan

for i in range(df_d2_soir.shape[0]):
        if i >= 31:
            moy_mois=[]
            for j in range(1,32):
                moy_mois.append(df_d2_soir['CA_TTC'][i-j])
            df_d2_soir['moyen_31_services'][i]=mean(moy_mois)
        else:
            df_d2_soir['moyen_31_services'][i]=np.nan

#Concat
df_d2 = pd.concat([df_d2_midi, df_d2_soir])
df_d2 = df_d2.sort_values(by='date')
df_d2 = df_d2.reset_index(drop=True)

#------ D16 data financières --------------------

df_d16['moyen_7_services'] = 0
df_d16['moyen_31_services'] = 0

#Split
df_d16_midi = df_d16[df_d16['service']=='midi'].reset_index(drop=True)
df_d16_soir = df_d16[df_d16['service']=='soir'].reset_index(drop=True)

#For loops pour créer les colonnes
for i in range(df_d16_midi.shape[0]):
        if i >= 7:
            moy_service=[]
            for j in range(1,8):
                moy_service.append(df_d16_midi['CA_TTC'][i-j])
            df_d16_midi['moyen_7_services'][i]=mean(moy_service)
        else:
            df_d16_midi['moyen_7_services'][i]=np.nan

for i in range(df_d16_midi.shape[0]):
        if i >= 31:
            moy_mois=[]
            for j in range(1,32):
                moy_mois.append(df_d16_midi['CA_TTC'][i-j])
            df_d16_midi['moyen_31_services'][i]=mean(moy_mois)
        else:
            df_d16_midi['moyen_31_services'][i]=np.nan

for i in range(df_d16_soir.shape[0]):
        if i >= 7:
            moy_service=[]
            for j in range(1,8):
                moy_service.append(df_d16_soir['CA_TTC'][i-j])
            df_d16_soir['moyen_7_services'][i]=mean(moy_service)
        else:
            df_d16_soir['moyen_7_services'][i]=np.nan

for i in range(df_d16_soir.shape[0]):
        if i >= 31:
            moy_mois=[]
            for j in range(1,32):
                moy_mois.append(df_d16_soir['CA_TTC'][i-j])
            df_d16_soir['moyen_31_services'][i]=mean(moy_mois)
        else:
            df_d16_soir['moyen_31_services'][i]=np.nan

#Concat
df_d16 = pd.concat([df_d16_midi, df_d16_soir])
df_d16 = df_d16.sort_values(by='date')
df_d16 = df_d16.reset_index(drop=True)

#------ Moyenne 3 derniers jours et services

def moyenne_(df):
    moye=[]
    for i in range(len(df)):
        if i >= 4:
            runningmoy=[]
            for j in range(1,4):

                runningmoy.append(df['CA_TTC'].iloc[i-j])
            moye.append(round(mean(runningmoy),2))
        else:
            moye.append(np.nan)
    return moye


df = df_d16
df2 = df_d2

new_df = pd.DataFrame()
for s in list(set(df.service)):
    for i in list(set(df.jour)):
        df_f = df[(df.jour == i) & (df.service == s)].reset_index(drop=True)
        df_f['moyenne_3der_j&service'] = moyenne_(df_f)
        new_df = pd.concat([new_df,df_f])

new_df2 = pd.DataFrame()
for s in list(set(df2.service)):
    for i in list(set(df2.jour)):
        df_f = df2[(df2.jour == i) & (df2.service == s)].reset_index(drop=True)
        df_f['moyenne_3der_j&service'] = moyenne_(df_f)
        new_df2 = pd.concat([new_df2,df_f])

df_d2 = new_df2.sort_values(by='date')
df_d16 = new_df.sort_values(by='date')

#---- To CSV --------------------------------------

df_d16.to_csv('../raw_data/df_feat_d16.csv', index=False)

df_d2.to_csv('../raw_data/df_feat_d2.csv', index=False)
