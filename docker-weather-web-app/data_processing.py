import requests
from api_key_handler import get_api_key

def get_weather_data(location):
    """
    get raw data from weather server
    :param location: entered by user
    :return: data from weather server if found, None if not. error code if any.
    """
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {'q': location, 'units': 'metric', 'appid': get_api_key()}
    response = requests.get(forecast_url, params=params)

    if response.status_code == 200:
        return response.json(), None
    else:
        return None, response.status_code

def process_forecast_data(forecast_list):
    """
    filtering relevant data out of the raw data taken from weather server
    :param forecast_list: raw data taken from weather server
    :return: summary of filtered data
    """
    daily_summaries = {}
    for entry in forecast_list:
        date_time = entry['dt_txt']
        date, time = date_time.split(' ')
        if date not in daily_summaries:
            daily_summaries[date] = {
                'date': date,
                'temp_mor': None,
                'temp_eve': None,
                'humidity_mor': None,
                'humidity_eve': None
            }
        if time == '09:00:00':
            daily_summaries[date]['temp_mor'] = entry['main']['temp']
            daily_summaries[date]['humidity_mor'] = entry['main']['humidity']
        if time == '18:00:00':
            daily_summaries[date]['temp_eve'] = entry['main']['temp']
            daily_summaries[date]['humidity_eve'] = entry['main']['humidity']
    return list(daily_summaries.values())
