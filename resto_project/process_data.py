import pandas as pd
import requests
import numpy as np
import datetime as dt

def historical_data(path):
    historical_data = pd.read_csv('../raw_data/448f97988afe977af36cfc73cde95211.csv')
    historical_data['dt'] = pd.to_datetime(historical_data['dt'], unit='s')
    lunch = historical_data[historical_data['dt'].dt.hour==12]
    dinner = historical_data[historical_data['dt'].dt.hour==18]

    lunch['service']='midi'
    dinner['service']='soir'

    historical_services = pd.concat([lunch, dinner])

    historical_services = historical_services.sort_values('dt')

    historical_services['dt'] = historical_services['dt'].dt.date
    historical_services = historical_services.set_index('dt')

    historical_services=historical_services.drop(columns=['timezone','dt_iso','lat','city_name','lon','pressure','sea_level','grnd_level','humidity','wind_deg','rain_1h','rain_3h','snow_1h','snow_3h','weather_id','weather_icon'])
    historical_services=historical_services.reset_index()
    historical_services=historical_services.rename(columns={'dt':'date'})

    return historical_services
    #historical_services.to_csv('Historical-services.csv', index=False)

def jour_annee(x):
    return x.toordinal() - dt.date(x.year, 1, 1).toordinal() + 1

def fetch_data_api(api, city, nodays):
    """
    Get weather data from weather API. Returns empty string if data not found'

    """
    #api = '7aa7fc7be1af4500882144440212208'
    #city = 'Paris'
    #nodays = '7'
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api}&q={city}&days={nodays}&aqi=no&alerts=no'

    response = requests.get(url)

    if response.status_code != 200:
        return ''
    data = response.json()

    data = data['forecast']['forecastday']
    return data

def process_api_forecast():
    data = fetch_data_api('ff3e7f86602e4b0bb4e82520210109','Paris','7')
    exo_data = pd.read_csv('../exo_data/events_exo_pred.csv')
    df_d2_sept=pd.read_csv('../raw_data/df_d2_sept.csv').tail(14).reset_index(drop=True)
    df_d16_sept=pd.read_csv('../raw_data/df_d16_sept.csv').tail(14).reset_index(drop=True)
    #print(df_d2_sept)
    daily_data = pd.DataFrame(data[0]['day']).iloc[2,:]
    ### gives the weather hour by hour for the entire first day###

    daily_hourly_data = pd.DataFrame(data[0]['hour'])
    #condition has a code and an image, the code below only keeps the needed weather state
    for i in range(len(daily_hourly_data)):
        interm = daily_hourly_data['condition'][i]['text']
        daily_hourly_data['condition'][i]=interm

    #condition is given as three values this keeps only one
    data_series=[]
    for i in range(7):
        data_series.append(data[i]['hour'])

    #condition has a code and an image, the code below only keeps the needed weather state
    for x in range(7):
        for y in range(24):
            data_series[x][y]['condition']=data_series[x][y]['condition']['text']

    d={}
    for i in range(len(data_series)):
        d[i] = pd.DataFrame(data_series[i])

    seven_day_forecast = pd.concat([d[i] for i in range(len(data_series))])

    #convert time column to datetime
    seven_day_forecast['time']=pd.to_datetime(seven_day_forecast['time'])

    #change conditions for a more simple range of possible values
    clear = ['Clear', 'Sunny']
    clouds = ['Clouds','Partly cloudy', 'Cloudy', 'Overcast']
    rain = ['Rain','Patchy rain possible', 'Patchy light rain', 'Light rain', 'Moderate rain at times','Moderate rain','Heavy rain at times','Heavy rain','Moderate or heavy rain shower','Torrential rain shower']
    mist = ['Mist']
    drizzle = ['Drizzle','Patchy light drizzle','Light drizzle','Freezing drizzle','Heavy freezing drizzle','Light rain shower']
    fog = ['Fog', 'Freezing Fog']
    snow = ['Snow','Patchy snow possible', 'Patchy sleet possible', 'Patchy freezing drizzle possible', 'Blowing snow','Blizzard','Moderate or heavy freezing rain','Light freezing rain','Light sleet', 'Moderate or heavy sleet','Patchy light snow','Light snow','Patchy moderate snow','Moderate snow','Patchy heavy snow','Heavy snow','Ice pellets','Light sleet showers', 'Moderate or heavy sleet showers','Light snow showers','Moderate or heavy snow showers','Light showers of ice pellets','Moderate or heavy showers of ice pellets']
    thunderstorm = ['Thunderstorm','Thundery outbreaks possible', 'Patchy light rain with thunder','Moderate or heavy rain with thunder','Patchy light snow with thunder','Moderate or heavy snow with thunder']
    haze = ['Haze']

    summed_conditions = [clear, clouds, rain, mist, drizzle, fog, snow, thunderstorm, haze]
    seven_day_forecast=seven_day_forecast.reset_index()
    for i in range(len(seven_day_forecast['condition'])):
        for x in summed_conditions:
            if seven_day_forecast['condition'][i] in x:
                seven_day_forecast['condition'][i] = x[0]

############################# SERVICE CREATION ####################
    lunch = seven_day_forecast[seven_day_forecast['time'].dt.hour==12]
    lunch['service']='midi'
    dinner = seven_day_forecast[seven_day_forecast['time'].dt.hour==18]
    dinner['service']='soir'

    forecasted_services = pd.concat([lunch, dinner])
    forecasted_services['time'] = forecasted_services['time'].dt.date
############################ CREATE COLUMNS FOR DATE, TIME, WEEK ... ########
    forecasted_services=forecasted_services.set_index('time')
    forecasted_services = forecasted_services.sort_values('time')
    forecasted_services = forecasted_services[['index','temp_c','condition','wind_kph','feelslike_c', 'service']]
    forecasted_services=forecasted_services.reset_index().rename(columns={'time':'date'}).drop(columns='index')
    forecasted_services=forecasted_services.rename(columns={'feelslike_c':'feels_like','temp_c':'temp', 'wind_kph':'wind_speed'}, errors = 'raise')
    forecasted_services['date'] = pd.to_datetime(forecasted_services['date'],  format='%Y-%m-%d')
    forecasted_services['jour_de_sem'] = forecasted_services['date'].dt.weekday +1
    forecasted_services['jour_du_mois'] = forecasted_services['date'].dt.day
    forecasted_services['mois_de_annee'] = forecasted_services['date'].dt.month
    forecasted_services['sem_de_annee'] = forecasted_services['date'].dt.week
    forecasted_services['jour_annee'] = forecasted_services.apply(lambda x:jour_annee(x['date']), axis=1)
    forecasted_services['temp_min'] = forecasted_services['temp'] - 1
    forecasted_services['temp_max'] = forecasted_services['temp'] + 1

    summed_conditions = ['clear', 'clouds', 'rain', 'mist', 'drizzle', 'fog', 'snow', 'thunderstorm', 'haze','drizzle_and_rain']

    ##################### TRANSFORM WEATHER CONDITION INTO ENCODED COLUMNS ####################

    forecasted_services['condition'] = forecasted_services['condition'].str.lower()
    table = pd.get_dummies(forecasted_services['condition'])
    forecasted_services = pd.merge(forecasted_services, table, left_index=True, right_index=True).drop(columns='condition')
    for i in summed_conditions:
        if i in forecasted_services:
            pass
        else:
            forecasted_services[i] = 0
    forecasted_services['jour']= forecasted_services['date'].dt.strftime('%A')


    ################### CLOUDS ALL CREATION ###########################
    forecasted_services['clouds_all'] = 0
    for i in range(len(forecasted_services)):
        if forecasted_services['clouds'][i]==1:
            forecasted_services['clouds_all'][i] = 50
        if forecasted_services['rain'][i]==1:
            forecasted_services['clouds_all'][i] = 50
        if forecasted_services['snow'][i]==1:
            forecasted_services['clouds_all'][i] = 50
        if forecasted_services['thunderstorm'][i]==1:
            forecasted_services['clouds_all'][i] = 50
    forecasted_services_d16 = forecasted_services.copy()
    forecasted_services_d2 = forecasted_services.copy()
    ########################WEATHER####################################

    forecasted_services_d16['clear'] = forecasted_services_d16['clear'].replace(1, 'sky is clear')

    forecasted_services_d16['clouds'] = forecasted_services_d16['clouds'].replace(1, 'overcast clouds')

    forecasted_services_d16['drizzle'] = forecasted_services_d16['drizzle'].replace(1, 'light intensity drizzle')

    forecasted_services_d16['drizzle_and_rain'] = forecasted_services_d16['drizzle_and_rain'].replace(1, 'light intensity drizzle rain')

    forecasted_services_d16['fog'] = forecasted_services_d16['fog'].replace(1, 'fog')

    forecasted_services_d16['mist'] = forecasted_services_d16['mist'].replace(1, 'mist')

    forecasted_services_d16['thunderstorm'] = forecasted_services_d16['thunderstorm'].replace(1, 'proximity thunderstorm')

    forecasted_services_d2['clear'] = forecasted_services_d2['clear'].replace(1, 'sky is clear')

    forecasted_services_d2['clouds'] = forecasted_services_d2['clouds'].replace(1, 'overcast clouds')

    forecasted_services_d2['drizzle'] = forecasted_services_d2['drizzle'].replace(1, 'light intensity drizzle')

    forecasted_services_d2['drizzle_and_rain'] = forecasted_services_d2['drizzle_and_rain'].replace(1, 'light intensity drizzle rain')

    forecasted_services_d2['fog'] = forecasted_services_d2['fog'].replace(1, 'fog')

    forecasted_services_d2['mist'] = forecasted_services_d2['mist'].replace(1, 'mist')

    forecasted_services_d2['thunderstorm'] = forecasted_services_d2['thunderstorm'].replace(1, 'proximity thunderstorm')

    ########################D2#########################################
    forecasted_services_d2['moyen_7_services'] = df_d2_sept['moyen_7_services']
    forecasted_services_d2['moyen_31_services'] = df_d2_sept['moyen_31_services']
    forecasted_services_d2['moyenne_3der_j&service'] = df_d2_sept['moyenne_3der_j&service']
    forecasted_services_d2['vacances_paris'] = 0

    exo_data['date']=pd.to_datetime(exo_data['date'])
    forecasted_services_d2 = forecasted_services_d2.merge(exo_data, how='left', left_on=['date','service'], right_on=['date','service'])

    forecasted_services_d2['jour'] = forecasted_services_d2['jour'].map({'Monday':'Lundi','Tuesday':'Mardi', 'Wednesday':'Mercredi','Thursday':'Jeudi','Friday':'Vendredi','Saturday':'Samedi','Sunday':'Dimanche'})
    forecasted_services_d2.to_csv('../raw_data/forecasted_services_d2.csv')



    ########################D16#########################################
    forecasted_services_d16['moyen_7_services'] = df_d16_sept['moyen_7_services']
    forecasted_services_d16['moyen_31_services'] = df_d16_sept['moyen_31_services']
    forecasted_services_d16['moyenne_3der_j&service'] = df_d16_sept['moyenne_3der_j&service']
    forecasted_services_d16['vacances_paris'] = 0

    exo_data['date']=pd.to_datetime(exo_data['date'])
    forecasted_services_d16 = forecasted_services_d16.merge(exo_data, how='left', left_on=['date','service'], right_on=['date','service'])

    forecasted_services_d16['jour'] = forecasted_services_d16['jour'].map({'Monday':'Lundi','Tuesday':'Mardi', 'Wednesday':'Mercredi','Thursday':'Jeudi','Friday':'Vendredi','Saturday':'Samedi','Sunday':'Dimanche'})
    forecasted_services_d16.to_csv('../raw_data/forecasted_services_d16.csv')



def PSG_Matches():
    championsl_2017=pd.read_csv('../raw_data/Fixtures/champions-league-2017-paris-saint-germain-CentralEuropeanStandardTime.csv')
    championsl_2018=pd.read_csv('../raw_data/Fixtures/champions-league-2018-paris-WEuropeStandardTime.csv')
    championsl_2019=pd.read_csv('../raw_data/Fixtures/champions-league-2019-paris-WEuropeStandardTime.csv')
    championsl_2020=pd.read_csv('../raw_data/Fixtures/champions-league-2020-paris-UTC.csv')
    ligue1_2018 = pd.read_csv('../raw_data/Fixtures/ligue-1-2018-paris-saint-germain-RomanceStandardTime.csv')
    ligue1_2019 = pd.read_csv('../raw_data/Fixtures/ligue-1-2019-paris-saint-germain-RomanceStandardTime.csv')
    ligue1_2020 = pd.read_csv('../raw_data/Fixtures/ligue-1-2020-paris-saint-germain-RomanceStandardTime.csv')
    ligue1_2021 = pd.read_csv('../raw_data/Fixtures/ligue-1-2021-paris-saint-germain-RomanceStandardTime.csv')

    all_series = [championsl_2017,championsl_2018,championsl_2019,championsl_2020, ligue1_2018,ligue1_2019,ligue1_2020,ligue1_2021]

    championsl_2017['Date']=pd.to_datetime(championsl_2017['Date'])
    championsl_2018['Date']=pd.to_datetime(championsl_2018['Date'])
    championsl_2019['Date']=pd.to_datetime(championsl_2019['Date'])
    championsl_2020['Date']=pd.to_datetime(championsl_2020['Date'])
    ligue1_2018['Date']=pd.to_datetime(ligue1_2018['Date'])
    ligue1_2019['Date']=pd.to_datetime(ligue1_2019['Date'])
    ligue1_2020['Date']=pd.to_datetime(ligue1_2020['Date'])
    ligue1_2021['Date']=pd.to_datetime(ligue1_2021['Date'])

    championsl_2017['Service']= 'Dinner'
    championsl_2018['Service']='Dinner'
    championsl_2019['Service']='Dinner'
    championsl_2020['Service']='Dinner'
    ligue1_2018['Service']='Dinner'
    ligue1_2019['Service']='Dinner'
    ligue1_2020['Service']='Dinner'
    ligue1_2021['Service']='Dinner'

    championsl_2017['Date']=pd.to_datetime(championsl_2017['Date']).dt.date
    championsl_2018['Date']=pd.to_datetime(championsl_2018['Date']).dt.date
    championsl_2019['Date']=pd.to_datetime(championsl_2019['Date']).dt.date
    championsl_2020['Date']=pd.to_datetime(championsl_2020['Date']).dt.date
    ligue1_2018['Date']=pd.to_datetime(ligue1_2018['Date']).dt.date
    ligue1_2019['Date']=pd.to_datetime(ligue1_2019['Date']).dt.date
    ligue1_2020['Date']=pd.to_datetime(ligue1_2020['Date']).dt.date
    ligue1_2021['Date']=pd.to_datetime(ligue1_2021['Date']).dt.date

    all_matches_ligue1 = pd.concat([ ligue1_2018,ligue1_2019,ligue1_2020,ligue1_2021], join='outer')
    all_matches_championsleague = pd.concat([championsl_2017, championsl_2018, championsl_2019, championsl_2020], join='outer')

    all_matches_ligue1=pd.DataFrame(np.repeat(all_matches_ligue1.values,2,axis=0), columns=['Match Number','Round Number','Date','Location','Home Team','Away Team','Group''Result','Service'])
    all_matches_championsleague=pd.DataFrame(np.repeat(all_matches_championsleague.values,2,axis=0), columns=['Match Number','Round Number','Date','Location','Home Team','Away Team','Group','Result','Service'])

    all_matches_ligue1['Service']='diner'
    all_matches_championsleague['Service']='diner'

    all_matches_ligue1=all_matches_ligue1.rename(columns={'Date':'date'})
    all_matches_championsleague=all_matches_championsleague.rename(columns={'Date':'date'})

    all_matches_ligue1=all_matches_ligue1.rename(columns={'Service':'service'})
    all_matches_championsleague=all_matches_championsleague.rename(columns={'Service':'service'})

    all_matches_ligue1['Match Happening-L1'] = 1
    all_matches_championsleague['Match Happening-CL'] = 1

    for i in np.linspace(0,358,180):
        all_matches_ligue1['Match Happening-L1'][i]= 0

    for i in np.linspace(0,358,180):
        all_matches_championsleague['Match Happening-CL'][i]= 0

    for i in np.linspace(0,358,180):
        all_matches_ligue1['service'][i]='midi'
    for i in np.linspace(0,358,180):
        all_matches_championsleague['service'][i]='midi'

    all_matches_ligue1=all_matches_ligue1.drop(columns=['Location','Home Team','Away Team','Match Number','Round Number', 'Group','Result'])
    all_matches_championsleague=all_matches_championsleague.drop(columns=['Location','Home Team','Away Team','Match Number', 'Round Number', 'Group', 'Result'])

    return all_matches_ligue1, all_matches_championsleague
#all_matches_ligue1.to_csv('PSG-Matches-Ligue1.csv',index=False)
#all_matches_championsleague.to_csv('PSG-Matches-CL.csv',index=False)


if __name__ == '__main__':
    #fetch_data_api()
    process_api_forecast()
