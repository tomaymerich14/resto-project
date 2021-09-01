from os import pathconf
import pandas as pd
import numpy as np


def excel_to_csv(filename):
    '''read raw EXCEL file from raw_data directory and return a clean CSV file in the raw_data directory
        filename as input : "CA_DarocoBourse" or CA_DarocoXVI"
    '''


    #absolute path = f'/Users/guillaume/code/tomaymerich14/resto-project/raw_data/{filename}.xlsx'
    path = f'../raw_data/{filename}.xlsx'
    df=pd.read_excel(path)


    #----------VARIABLES DE PREPRO------------
    service_dict = {
    '[09h à 10h[':'midi','[10h à 11h[':'midi','[11h à 12h[':'midi','[12h à 13h[':'midi','[13h à 14h[':'midi',
    '[14h à 15h[':'midi','[15h à 16h[':'midi','[16h à 17h[':'midi','[17h à 18h[':'midi',
    '[18h à 19h[':'soir','[19h à 20h[':'soir','[20h à 21h[':'soir','[21h à 22h[':'soir','[22h à 23h[':'soir',
    '[23h à 00h[':'soir','[00h à 01h[':'soir','[01h à 02h[':'soir','[02h à 03h[':'soir','[03h à 04h[':'soir',
    }
    Week_days={'Lundi':'Dimanche','Mardi':'Lundi','Mercredi':'Mardi','Jeudi':'Mercredi','Vendredi':'Jeudi','Samedi':'Vendredi','Dimanche':'Samedi'}
    #----------------------------------------



    #----------Adding Datetime Column------------
    df['Date']=''
    for i in range(df.shape[0]):
        df['Date'][i] = f"{df['Jour du mois'][i]}-{df['Mois'][i]}-{df['Année'][i]}"
    df['Date']=pd.to_datetime(df['Date'],format='%d-%m-%Y',dayfirst=True)
    #----------------------------------------

    #----------Mapping chaque Tranche Horaire à un Service [Midi] ou [Soir]-------
    df['Service']=df['Tranche Horaire'].map(service_dict)
    #-----------------------------------------

    #----------Recalage des Date en fonction des tranches horaires qui dépassent minuit-------
    df['Date']=np.where(df['Tranche Horaire']=='[00h à 01h[',df['Date']- pd.offsets.Day(1),df['Date'])
    df['Date']=np.where(df['Tranche Horaire']=='[01h à 02h[',df['Date']- pd.offsets.Day(1),df['Date'])
    df['Date']=np.where(df['Tranche Horaire']=='[02h à 03h[',df['Date']- pd.offsets.Day(1),df['Date'])
    df['Date']=np.where(df['Tranche Horaire']=='[03h à 04h[',df['Date']- pd.offsets.Day(1),df['Date'])
    #-----------------------------------------

    #----------Drop Colonnes maintenant redondantes et inexactes--------------
    df=df.drop(columns=['Année','Mois','Jour du mois'])
    #------------------------------------------



    #--------------Recalage des Jours de la semaine en fonction des tranches horaires qui dépassent minuit--
    df.loc[df['Tranche Horaire'] == '[00h à 01h[','Jour de la semaine']=\
    df.loc[df['Tranche Horaire'] == '[00h à 01h[']['Jour de la semaine'].map(Week_days)

    df.loc[df['Tranche Horaire'] == '[01h à 02h[','Jour de la semaine']=\
    df.loc[df['Tranche Horaire'] == '[01h à 02h[']['Jour de la semaine'].map(Week_days)

    df.loc[df['Tranche Horaire'] == '[02h à 03h[','Jour de la semaine']=\
    df.loc[df['Tranche Horaire'] == '[02h à 03h[']['Jour de la semaine'].map(Week_days)

    df.loc[df['Tranche Horaire'] == '[03h à 04h[','Jour de la semaine']=\
    df.loc[df['Tranche Horaire'] == '[03h à 04h[']['Jour de la semaine'].map(Week_days)
    #----------------------------------

    #----------------Adding unique 'Timestamp' index for each service with [hour=12] or [hour=18]-------------
    df['Timestamp']=np.where(df['Service']=='midi',\
                                df['Date']+pd.tseries.offsets.DateOffset(hours=12),\
                                df['Date']+pd.tseries.offsets.DateOffset(hours=18))
    df=df.set_index('Timestamp')
    df.sort_index(inplace=True)
    #-----------------------------------------------------------

    #-------------------Sum() Groupby on Timestamp------------------
    df=df.groupby(['Timestamp','Date','Jour de la semaine','Service']).sum()
    #----------------------------------

    #-------------------rounding------
    df['CA TTC'] = round(df['CA TTC'], 2)
    df['CA HT']=round(df['CA HT'],2)
    df['TVA']=round(df['TVA'],2)

    #----------------------------------

    #-------------Setting Correct unique 'Timestamp' index
    df=df.reset_index(level=[1,2,3])
    #------------------------------------------

    #-------------Renaming Columns-------
    df=df.rename(columns={"Date": "date", "Jour de la semaine": "jour","Service":"service","CA TTC":"CA_TTC","CA HT":"CA_HT"})
    #-------------



    #----------------------------------------#----------------------------------------
    #----------MODIFICATIONS PROPRE A DarocoBourse-------------- #----------------------------------------
    if filename == 'CA_DarocoBourse':


        #----------------------------------------#----------------------------------------
        #----------CHhoix des BORNES de notre DATASET DAROCO Bourse-------------- -----------

        # DEBUT 2019-01-01, FIN 2021-07-31
        df = df[(df.index >= "2019-01-01 12:00:00") & (df.index <= "2021-07-31 18:00:00")]

        #----------------------------------------#----------------------------------------
        #----------------------------------------#----------------------------------------


        #----------------------------------------#----------------------------------------
        #----------Drop LIGNES DE MIDI DE BOURSE OUTLIERS-------------- #----------------------------------------
        midi_df_dBourse = df[ df['service'] == 'midi' ]
        midi_df_dB_index_CA_petit=midi_df_dBourse[ midi_df_dBourse['CA_TTC'] < 500 ].index
        df=df.drop(midi_df_dB_index_CA_petit)

        midi_df_dB_index_CA_grand=midi_df_dBourse[ midi_df_dBourse['CA_TTC'] > 8500 ].index
        df=df.drop(midi_df_dB_index_CA_grand)
        #----------------------------------------#----------------------------------------
        #----------------------------------------#----------------------------------------

        #----------------------------------------#----------------------------------------
        #----------Drop LIGNES DE SOIR DE BOURSE OUTLIERS-------------- #----------------------------------------

        soir_df_dBourse = df[ df['service'] == 'soir' ]

        soir_df_dB_index_CA_petit=soir_df_dBourse[ soir_df_dBourse['CA_TTC'] < 650 ].index
        df=df.drop(soir_df_dB_index_CA_petit)


        soir_df_dB_index_CA_grand=soir_df_dBourse[ soir_df_dBourse['CA_TTC'] > 17000 ].index
        df=df.drop(soir_df_dB_index_CA_grand)

        #----------------------------------------#----------------------------------------
        #----------------------------------------#----------------------------------------

        #----------------------------------------#----------------------------------------
        #----------Drop LIGNES Restrictions COVID Daroco Bourse----------- #----------------------------------------

        # DU 2020-03-14 au 2020-06-15 inclus
        df=df.drop(df[(df.index > "2020-03-14 18:00:00") & (df.index < "2020-06-15 12:00:00")].index)

        #----------------------------------------#----------------------------------------
        #--------------------------------------- #----------------------------------------



    #----------------------------------------#----------------------------------------
    #----------MODIFICATIONS PROPRE A DarocoXVI-------------- #----------------------------------------
    if filename == 'CA_DarocoXVI':

        #----------------------------------------#----------------------------------------
        #----------Choix des BORNES de notre DATASET DAROCO XVI-------------- -----------

        # DEBUT 2019-09-01, FIN 2021-07-31
        df = df[(df.index >= "2019-09-01 12:00:00") & (df.index <= "2021-07-31 18:00:00")]

        #----------------------------------------#----------------------------------------
        #----------------------------------------#----------------------------------------

        #----------------------------------------#----------------------------------------
        #----------Drop LIGNES DE MIDI DE XVI OUTLIERS-------------- #----------------------------------------
        midi_df_dXVI = df[df['service'] == 'midi']

        midi_df_dXVI_index_CA_petit=midi_df_dXVI[ midi_df_dXVI['CA_TTC'] < 600 ].index
        df = df.drop(midi_df_dXVI_index_CA_petit)

        midi_df_dXVI_index_CA_grand=midi_df_dXVI[ midi_df_dXVI['CA_TTC'] > 7000 ].index
        df = df.drop(midi_df_dXVI_index_CA_grand)
        #----------------------------------------#----------------------------------------
        #----------------------------------------#----------------------------------------

        #----------------------------------------#----------------------------------------
        #----------Drop LIGNES DE SOIR DE XVI OUTLIERS-------------- #----------------------------------------

        soir_df_dXVI = df[df['service'] == 'soir']

        soir_df_dXVI_index_CA_petit=soir_df_dXVI[ soir_df_dXVI['CA_TTC'] < 700 ].index
        df = df.drop(soir_df_dXVI_index_CA_petit)


        soir_df_dXVI_index_CA_grand=soir_df_dXVI[ soir_df_dXVI['CA_TTC'] > 14000 ].index
        df = df.drop(soir_df_dXVI_index_CA_grand)

        #----------------------------------------#----------------------------------------
        #----------------------------------------#----------------------------------------

        #----------------------------------------#----------------------------------------
        #----------Drop LIGNES Restrictions COVID Daroco XVI----------- #----------------------------------------
        # DROP DU 2020-03-14 au 2020-06-06
        df=df.drop(df[(df.index >= "2020-03-14 12:00:00") & (df.index <= "2020-06-06 18:00:00")].index)

        # DROP DU 2021-05-19 au 2021-06-08
        df=df.drop(df[(df.index >= "2021-05-19 12:00:00") & (df.index <= "2021-06-08 18:00:00")].index)
        #----------------------------------------#----------------------------------------
        #--------------------------------------- #----------------------------------------



    #-------------------------Create CSV in RAW_DATA directory------------------------------
    if filename == 'CA_DarocoBourse':
        df.to_csv(r'../raw_data/df_raw_d2.csv',index=False)


    if filename == 'CA_DarocoXVI':
        df.to_csv(r'../raw_data/df_raw_d16.csv', index=False)



    return None




if __name__ == '__main__':


    excel_to_csv('CA_DarocoBourse')
    excel_to_csv('CA_DarocoXVI')




    #TEST
    #df.to_csv(r'/Users/guillaume/Desktop/Projet_Daroco/df_dBourse_test.csv',index=False)
    #df.to_csv(r'/Users/guillaume/Desktop/Projet_Daroco/df_DXVI_test.csv',index=False)
