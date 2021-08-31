weather_sorted = {
    'Clear': ['sky is clear', np.nan, np.nan, np.nan],
    'Clouds':
    ['scattered clouds', 'few clouds', 'broken clouds', 'overcast clouds'],
    'Drizzle':
    ['light intensity drizzle', 'drizzle', 'heavy intensity drizzle', np.nan],
    'Drizzle and Rain':
    ['light intensity drizzle rain', 'rain and drizzle', np.nan, np.nan],
    'Fog': ['fog', np.nan, np.nan, np.nan],
    'Haze': ['haze', np.nan, np.nan, np.nan],
    'Mist': ['mist', np.nan, np.nan, np.nan],
    'Rain': [
        'light rain', 'light intensity shower rain', 'moderate rain',
        'heavy intensity rain'
    ],
    'Snow': ['light snow', np.nan, np.nan, np.nan],
    'Thunderstorm': [
        'proximity thunderstorm', 'thunderstorm',
        'thunderstorm with light rain', 'thunderstorm with heavy rain'
    ]
}

def weather_cat(x, list_values):
    for values in list_values:
        if x == values:
            return values

def weather_col(df):
    for i in range(len(list(weather_sorted.values()))):
        nom_col = list(weather_sorted.keys())[i]
        list_col = list(weather_sorted.values())[i]
        df[nom_col] = df.apply(lambda x: weather_cat(x['weather_description'], list_col), axis=1)
        pass
