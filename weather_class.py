import pandas as pd 

stadiums_dict = {
    'ARI': 'https://forecast.weather.gov/MapClick.php?lat=33.4452&lon=-112.0668&lg=english&&FcstType=digital',
    'ANA': 'https://forecast.weather.gov/MapClick.php?lat=33.7994&lon=-117.8839&lg=english&&FcstType=digital',
    'ATL': 'https://forecast.weather.gov/MapClick.php?lat=33.8908&lon=-84.468&lg=english&&FcstType=digital',
    'BAL': 'https://forecast.weather.gov/MapClick.php?lat=39.2838&lon=-76.6223&lg=english&&FcstType=digital',
    'BOS': 'https://forecast.weather.gov/MapClick.php?lat=42.3468&lon=-71.0986&lg=english&&FcstType=digital',
    'CHC': 'https://forecast.weather.gov/MapClick.php?lat=41.94816000000003&lon=-87.65564999999998&lg=english&&FcstType=digital',
    'CHW': 'https://forecast.weather.gov/MapClick.php?lat=41.83&lon=-87.6337&lg=english&&FcstType=digital',
    'CIN': 'https://forecast.weather.gov/MapClick.php?lat=39.0973&lon=-84.5067&lg=english&&FcstType=digital',
    'CLE': 'https://forecast.weather.gov/MapClick.php?lat=41.4955&lon=-81.6853&lg=english&&FcstType=digital',
    'COL': 'https://forecast.weather.gov/MapClick.php?lat=39.7547&lon=-104.9945&lg=english&&FcstType=digital',
    'DET': 'https://forecast.weather.gov/MapClick.php?lat=42.3378&lon=-83.0512&lg=english&&FcstType=digital',
    'FLA': 'https://forecast.weather.gov/MapClick.php?lat=25.7781&lon=-80.2195&lg=english&&FcstType=digital',
    'HOU': 'https://forecast.weather.gov/MapClick.php?lat=29.757&lon=-95.3566&lg=english&&FcstType=digital',
    'KCR': 'https://forecast.weather.gov/MapClick.php?lat=39.0516&lon=-94.4827&lg=english&&FcstType=digital',
    'LAD': 'https://forecast.weather.gov/MapClick.php?lat=34.0862&lon=-118.2436&lg=english&&FcstType=digital',
    'MIL': 'https://forecast.weather.gov/MapClick.php?lat=43.0297&lon=-87.9725&lg=english&&FcstType=digital',
    'MIN': 'https://forecast.weather.gov/MapClick.php?lat=44.982&lon=-93.2777&lg=english&&FcstType=digital',
    'NYM': 'https://forecast.weather.gov/MapClick.php?lat=40.757&lon=-73.8459&lg=english&&FcstType=digital',
    'NYY': 'https://forecast.weather.gov/MapClick.php?lat=40.8309&lon=-73.9269&lg=english&&FcstType=digital',
    'OAK': 'https://forecast.weather.gov/MapClick.php?lat=37.7503&lon=-122.2029&lg=english&&FcstType=digital',
    'PHI': 'https://forecast.weather.gov/MapClick.php?lat=39.9059&lon=-75.1665&lg=english&&FcstType=digital',
    'PIT': 'https://forecast.weather.gov/MapClick.php?lat=40.4476&lon=-80.005&lg=english&&FcstType=digital',
    'SDP': 'https://forecast.weather.gov/MapClick.php?lat=32.707&lon=-117.1561&lg=english&&FcstType=digital',
    'SFG': 'https://forecast.weather.gov/MapClick.php?lat=37.7781&lon=-122.3908&lg=english&&FcstType=digital',
    'SEA': 'https://forecast.weather.gov/MapClick.php?lat=47.5911&lon=-122.3342&lg=english&&FcstType=digital',
    'STL': 'https://forecast.weather.gov/MapClick.php?lat=38.6236&lon=-90.193&lg=english&&FcstType=digital',
    'TBD': 'https://forecast.weather.gov/MapClick.php?lat=27.7682&lon=-82.6533&lg=english&&FcstType=digital',
    'TEX': 'https://forecast.weather.gov/MapClick.php?lat=32.746&lon=-97.0827&lg=english&&FcstType=digital',
    'TOR': 'https://forecast.weather.gov/MapClick.php?lat=42.8805&lon=-78.8738&lg=english&&FcstType=digital',
    'WSN': 'https://forecast.weather.gov/MapClick.php?lat=38.8724&lon=-77.0085&lg=english&&FcstType=digital'
} 


class weather:
    def __init__(self, team_abbr, url):
        self.team_abbr = team_abbr
        self.url = url

    def get_weather(self):
        # Get initial DataFrame
        weather_dfs = pd.read_html(self.url, header=None, index_col = None)
        stadium_weather_df = weather_dfs[7].copy()
        del weather_dfs

        # Find rows to transpose
        stadium_weather_df.insert(0, 'row_num', range(0,len(stadium_weather_df))) # add row_num
        rows_to_copy = stadium_weather_df[['row_num']][stadium_weather_df[0] == 'Date'].copy()
        rows_to_copy = rows_to_copy.reset_index().drop(['index'], axis=1)
        rows_to_copy['row_num'][1] = rows_to_copy['row_num'][1]-2

        # Drop row_num
        stadium_weather_df = stadium_weather_df.drop('row_num', axis=1)

        # transpose the dataframe
        stadium_weather_copy_df = stadium_weather_df.loc[rows_to_copy['row_num'][0]:rows_to_copy['row_num'][1], :].T.copy()
        del stadium_weather_df

        # Create Propper Header
        stadium_weather_copy_df = stadium_weather_copy_df.rename(columns=stadium_weather_copy_df.iloc[0])

        # Drop Redundant first row
        stadium_weather_copy_df = stadium_weather_copy_df.drop([0])

        # Replace NaN in Date
        ## Get Dates
        dates_df = pd.DataFrame(columns=['Date'])
        for i in stadium_weather_copy_df['Date']:
            if type(i) == str:
                SR_row = pd.Series({'Date' : i})
                dates_df = dates_df.append(SR_row,ignore_index=True)
        ## Get Row Numbers of NaN
        date_row_num = pd.DataFrame(columns=['row_num'])
        for i in range(1,len(stadium_weather_copy_df['Date'])):
            if type(stadium_weather_copy_df['Date'][i]) == str:
                SR_row = pd.Series({'row_num' : i})
                date_row_num = date_row_num.append(SR_row,ignore_index=True)
        date_row_num = date_row_num.append(pd.Series({'row_num' : len(stadium_weather_copy_df['Date'])}),ignore_index=True)      

        for i in range(1,(len(dates_df)+1)):
            if i == 1:
                stadium_weather_copy_df['Date'][(date_row_num['row_num'][1-1]-1):date_row_num['row_num'][1]].fillna(dates_df['Date'][i-1], inplace = True)
            if i == 2:
                if date_row_num['row_num'][1] != 24:
                    stadium_weather_copy_df['Date'][date_row_num['row_num'][(2-1)]:date_row_num['row_num'][2]].fillna(dates_df['Date'][i-1], inplace = True)

        # Replace other NaN with '--'
        stadium_weather_copy_df.fillna('--', inplace = True)

        # Remove the degrees sign
        keys = ['Date', 'Hour (CDT)', 'Temperature (°F)', 'Dewpoint (°F)', 'Wind Chill (°F)', 'Surface Wind (mph)',
                'Wind Dir', 'Gust', 'Sky Cover (%)', 'Precipitation Potential (%)', 'Relative Humidity (%)',
                'Rain', 'Thunder', 'Snow', 'Freezing Rain', 'Sleet']
        values = ['Date', 'Hour (CDT)', 'Temperature (F)', 'Dewpoint (F)', 'Wind Chill (F)', 'Surface Wind (mph)', 'Wind Dir',
                'Gust', 'Sky Cover (pct)', 'Precipitation Potential (pct)', 'Relative Humidity (pct)', 'Rain', 'Thunder',
                'Snow', 'Freezing Rain', 'Sleet']
        dictionary = dict(zip(keys, values))
        stadium_weather_copy_df = stadium_weather_copy_df.rename(columns=dictionary)
        stadium_weather_copy_df.insert(0, 'Team', self.team_abbr)

        return(stadium_weather_copy_df)