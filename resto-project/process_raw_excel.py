from os import pathconf
import pandas as pd
import numpy as np

#'/Users/guillaume/code/tomaymerich14/resto-project/raw_data/CA_DarocoBourse.xlsx'

def excel_to_csv(filename):
    '''read raw EXCEL file from raw_data directory and return a clean CSV file in the raw_data directory
        filename as input : "CA_DarocoBourse" or CA_DarocoXVI"
    '''


    #path = f'/Users/guillaume/code/tomaymerich14/resto-project/raw_data/{filename}.xlsx'
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

    #----------Drop Colonnes maintenant redondantes--------------
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
    #----------Drop PREMIERE LIGNE DE BOURSE-------------- #----------------------------------------
    if filename == 'CA_DarocoBourse':
        df=df.sort_values(by='date')
        df=df.iloc[1: , :]
    #----------------------------------------#----------------------------------------
    #----------------------------------------#----------------------------------------



    #-------------------------Create CSV in RAW DATA------------------------------
    if filename == 'CA_DarocoBourse':
        df.to_csv(r'../raw_data/df_dBourse.csv',index=False)
    if filename == 'CA_DarocoXVI':
        df.to_csv(r'../raw_data/df_DXVI.csv', index=False)


    return None






#Console TEST
if __name__ == '__main__':

    #path = '/Users/guillaume/code/tomaymerich14/resto-project/raw_data/CA_DarocoBourse.xlsx'

    #TEST

    excel_to_csv('CA_DarocoBourse')
    excel_to_csv('CA_DarocoXVI')
    #df.to_csv(r'/Users/guillaume/Desktop/Projet_Daroco/df_dBourse.csv',index=False)
    #df.to_csv(r'/Users/guillaume/Desktop/Projet_Daroco/df_DXVI.csv',index=False)
