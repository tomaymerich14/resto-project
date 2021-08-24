import pandas as pd
import numpy as np

def merge():

    events = pd.read_csv('../exo_data/events.csv')
    hist_meteo = pd.read_csv('../exo_data/Historical-Services.csv')
    psg = pd.read_csv('../exo_data/PSG-Matches.csv')
    psg_ldc =  pd.read_csv('../exo_data/PSG-Matches-CL.csv')
    db = pd.read_csv('../raw_data/df_dBourse.csv')
    d16 =pd.read_csv('../raw_data/df_DXVI.csv')
    vac = pd.read_csv('../exo_data/vacances_paris.csv')

    # --------------- TO OPERATE BEFORE --------------------

    # Drop columns All Matchs PSG
    psg = psg.drop(columns=['Location','Home Team', 'Away Team'])
    # Drop columns Vacs
    vac = vac.drop(columns=['Unnamed: 0'])
    # Duplicate lines vacs
    vac = pd.DataFrame(np.repeat(vac.values,2,axis=0),columns=['date','vacances_paris'])
    # Set diner
    vac['service']='diner'
    # Set midi
    for i in np.linspace(0,2920,1461):
        vac['service'][i]='midi'

    #-------------------------------------------------------

    # Merge d2
    df_d2 = db.merge(hist_meteo, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(events, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg, how='outer', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg_ldc, how='outer', left_on=["date", "service"], right_on=["date","service"])\
    .merge(vac, how='left', left_on=["date", "service"], right_on=["date","service"])

    # Stop fin juillet
    df_d2 = df_d2[:1374]
    # OK pour d2

    # Merge d16
    df_d16 = d16.merge(hist_meteo, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(events, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg, how='outer', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg_ldc, how='outer', left_on=["date", "service"], right_on=["date","service"])\
    .merge(vac, how='left', left_on=["date", "service"], right_on=["date","service"])

    # Début ouverture, stop fin juillet
    df_d16 = df_d16[9:877]

    # --------------- CSV ------------------------------------

    #CSV preproc_data_d2
    df_d2.to_csv('../raw_data/preproc_data_d2.csv', index=False)

    #CSV preproc_data_d16
    df_d16.to_csv('../raw_data/preproc_data_d16.csv', index=False)

    pass

if __name__ == '__main__':
    merge()
