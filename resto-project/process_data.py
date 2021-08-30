import pandas as pd
import requests
import numpy as np

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

def fetch_data_api(api,city,nodays):
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

    return data['forecast']['forecastday']

def process_api_forecast():
    data = fetch_data_api('09e033659f124258acf74721212408','Paris','3')
    daily_data = pd.DataFrame(data[0]['day']).iloc[2,:]
    ### gives the weather hour by hour for the entire first day###

    daily_hourly_data = pd.DataFrame(data[0]['hour'])
    #condition has a code and an image, the code below only keeps the needed weather state
    for i in range(len(daily_hourly_data)):
        daily_hourly_data['condition'][i]=daily_hourly_data['condition'][i]['text']

    #condition is given as three values this keeps only one
    data_series=[]
    for i in range(3):
        data_series.append(data[i]['hour'])

    #condition has a code and an image, the code below only keeps the needed weather state
    for x in range(3):
        for y in range(24):
            data_series[x][y]['condition']=data_series[x][y]['condition']['text']

    d={}
    for i in range(len(data_series)):
        d[i] = pd.DataFrame(data_series[i])

    seven_day_forecast = pd.concat([d[i] for i in range(len(data_series))])

    #convert time column to datetime
    seven_day_forecast['time']=pd.to_datetime(seven_day_forecast['time'])

    #change conditions for a more simple range of possible values
    Clear = ['Clear', 'Sunny']
    Clouds = ['Clouds','Partly cloudy', 'Cloudy', 'Overcast']
    Rain = ['Rain','Patchy rain possible', 'Patchy light rain', 'Light rain', 'Moderate rain at times','Moderate rain','Heavy rain at times','Heavy rain','Moderate or heavy rain shower','Torrential rain shower']
    Mist = ['Mist']
    Drizzle = ['Drizzle','Patchy light drizzle','Light drizzle','Freezing drizzle','Heavy freezing drizzle','Light rain shower']
    Fog = ['Fog', 'Freezing Fog']
    Snow = ['Snow','Patchy snow possible', 'Patchy sleet possible', 'Patchy freezing drizzle possible', 'Blowing snow','Blizzard','Moderate or heavy freezing rain','Light freezing rain','Light sleet', 'Moderate or heavy sleet','Patchy light snow','Light snow','Patchy moderate snow','Moderate snow','Patchy heavy snow','Heavy snow','Ice pellets','Light sleet showers', 'Moderate or heavy sleet showers','Light snow showers','Moderate or heavy snow showers','Light showers of ice pellets','Moderate or heavy showers of ice pellets']
    Thunderstorm = ['Thunderstorm','Thundery outbreaks possible', 'Patchy light rain with thunder','Moderate or heavy rain with thunder','Patchy light snow with thunder','Moderate or heavy snow with thunder']
    Haze = ['Haze']

    summed_conditions = [Clear, Clouds, Rain, Mist, Drizzle, Fog, Snow, Thunderstorm, Haze]

    for i in range(len(seven_day_forecast['condition'])):
        for x in summed_conditions:
            if seven_day_forecast['condition'][i] in x:
                seven_day_forecast['condition'][i]=x[0]

    lunch = seven_day_forecast[seven_day_forecast['time'].dt.hour==12]
    lunch['Service']='Lunch'
    dinner = seven_day_forecast[seven_day_forecast['time'].dt.hour==18]
    dinner['Service']='Dinner'

    forecasted_services = pd.concat([lunch, dinner])
    forecasted_services['time'] = forecasted_services['time'].dt.date

    forecasted_services=forecasted_services.set_index('time')
    forecasted_services = forecasted_services.sort_values('time')

    return forecasted_services

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
