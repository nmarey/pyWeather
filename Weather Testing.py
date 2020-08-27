# %%
import weather_class
import pandas as pd
# %%
# import chi url
chc_url = weather_class.stadiums_dict['CHC']

# %%
# chc weather class
chc_weather = weather_class.weather('CHC', chc_url)

# %%
# Get the weather forecast for chc
weather_pd = chc_weather.get_weather()

# %%
# import the stadiums dict to loop through for the weather
stad_dict = weather_class.stadiums_dict

# %%
# Loop over the stad dict to get the weather
weather_dict = dict()

for k, v in stad_dict.items():
    loop_weather = weather_class.weather(k, v)
    loop_weather_pd = loop_weather.get_weather()
    weather_dict[k] = loop_weather_pd

# Errors out at line 82
# Error appears to stem from having two dates in the data frame
# Need a better way to manipulate df so only for 1 date
# %%
