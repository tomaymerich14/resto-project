import pandas as pd
from cyclical import cyclical_columns
def merge():

    db = pd.read_csv('../raw_data/df_feat_d2.csv')
    d16 =pd.read_csv('../raw_data/df_feat_d16.csv')
    #all_events = pd.read_csv('../exo_data/all_events_sport_and_weather.csv')
    data_weather = pd.read_csv('../exo_data/data_weather.csv')
    #data_sports = pd.read_csv('../exo_data/data_sports.csv')
    data_events = pd.read_csv('../exo_data/data_events.csv')
    data_vacances = pd.read_csv('../exo_data/data_vacances.csv')
    psg_matches = pd.read_csv('../exo_data/psg_matches.csv')
    psg_matches_cl = pd.read_csv('../exo_data/psg_matches_cl.csv')


    #-------------------------------------------------------

    # Merge d2
    df_d2 = db.merge(data_weather, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(data_events, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(data_vacances, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg_matches, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg_matches_cl, how='left', left_on=["date", "service"], right_on=["date","service"])


    # Pb avec météo, on drop duplicates
    df_d2 = df_d2.drop_duplicates(subset=['date', 'service'], keep='first')
    df_d2.drop(columns = ['CA_HT','TVA'], inplace= True)
    df_d2.drop(columns=['Location', 'Home Team', 'Away Team'], inplace=True)
    df_d2['Match Happening'].replace(to_replace=0.0,value=1,inplace=True)
    df_d2['Match Happening-CL'].replace(to_replace=0.0,value=1,inplace=True)
    df_d2['match_happening'] = df_d2['Match Happening'].copy()
    df_d2['match_happening_cl'] = df_d2['Match Happening-CL'].copy()
    df_d2.drop(columns=['Match Happening', 'Match Happening-CL'],inplace=True)
    df_d2.fillna(value=0, inplace=True)

    # Reset index
    df_d2 = df_d2.reset_index(drop=True)

    # Stop en fin juillet
    #df_d2 = df_d2[:df_d2.loc[df_d2['date']=='2021-07-31'].index[1]+1]
    # OK pour d2

    # Merge d16 ----------------------------------------------
    df_d16 = d16.merge(data_weather, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(data_events, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(data_vacances, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg_matches, how='left', left_on=["date", "service"], right_on=["date","service"])\
    .merge(psg_matches_cl, how='left', left_on=["date", "service"], right_on=["date","service"])

    df_d16 = df_d16.drop_duplicates(subset=['date', 'service'], keep='first')
    df_d16.drop(columns=['CA_HT', 'TVA'], inplace=True)
    df_d16.drop(columns=['Location', 'Home Team','Away Team'], inplace=True)
    df_d16['Match Happening'].replace(to_replace=0.0,value=1,inplace=True)
    df_d16['Match Happening-CL'].replace(to_replace=0.0,value=1,inplace=True)
    df_d16['match_happening'] = df_d16['Match Happening'].copy()
    df_d16['match_happening_cl'] = df_d16['Match Happening-CL'].copy()
    df_d16.drop(columns=['Match Happening', 'Match Happening-CL'], inplace=True)
    df_d16.fillna(value=0,inplace=True)

    df_d16 = df_d16.reset_index(drop=True)

    #df_d16 = df_d16[:df_d16.loc[df_d16['date']=='2021-07-31'].index[1]+1]

    # --------------- CSV ------------------------------------

    #CSV preproc_data_d2
    df_d2.to_csv('../raw_data/preproc_data_d2.csv', index=False)

    #CSV preproc_data_d16
    df_d16.to_csv('../raw_data/preproc_data_d16.csv', index=False)

    cyclical_columns()

    pass

if __name__ == '__main__':
    merge()
