import pandas as pd
import numpy as np

def merge():

    events = pd.read_csv('../exo_data/events.csv')
    weather_df = pd.read_csv('../exo_data/weather_df.csv')
    football_df = pd.read_csv('../exo_data/football_df.csv')
    db = pd.read_csv('../raw_data/df_dBourse.csv')
    d16 =pd.read_csv('../raw_data/df_DXVI.csv')
    vacation_df = pd.read_csv('../exo_data/vacation_df.csv')

    #-------------------------------------------------------

    # Merge d2
    df_d2 = db.merge(weather_df, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(events, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(football_df, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(vacation_df, how='left', left_on=["date","service"], right_on=["date","service"])

    # Pb avec météo, on drop duplicates
    df_d2 = df_d2.drop_duplicates(subset=['date', 'service'], keep='first')

    # Reset index
    df_d2 = df_d2.reset_index(drop=True)

    # Stop en fin juillet
    df_d2 = df_d2[:df_d2.loc[df_d2['date']=='2021-07-31'].index[1]+1]
    # OK pour d2

    # Merge d16 ----------------------------------------------
    df_d16 = d16.merge(weather_df, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(events, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(football_df, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(vacation_df, how='left', left_on=["date","service"], right_on=["date","service"])

    df_d16 = df_d16.drop_duplicates(subset=['date', 'service'], keep='first')

    df_d16 = df_d16.reset_index(drop=True)

    df_d16 = df_d16[:df_d16.loc[df_d16['date']=='2021-07-31'].index[1]+1]

    # --------------- CSV ------------------------------------

    #CSV preproc_data_d2
    df_d2.to_csv('../raw_data/preproc_data_d2.csv', index=False)

    #CSV preproc_data_d16
    df_d16.to_csv('../raw_data/preproc_data_d16.csv', index=False)

    pass

if __name__ == '__main__':
    merge()
