import requests
#We access the API KEY by doing the following
from dotenv import load_dotenv
import os
#We want to access the weather information in a clean way
from dataclasses import dataclass
import pycountry

#Pulls the data from the .env file
load_dotenv()
#Accesses the API key using this, loads it into api key
api_key = os.getenv('API_KEY')

#We use all these values to create a weather data object 
@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float

#To make a API call to find the current weather we need the latitude and longitude of the place we want, and but the way to get these
#is to use the direct geocoding API, this needs the name of the location (city name or area name).
#the '.json' converts the response into a .json object if it is possible
def get_lat_lon(cityName, countryCode, API_KEY): 
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={cityName},{countryCode}&appid={API_KEY}').json()

    #puts the json find into a list, then gets the lat on lon to use onwards
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon     #returns a tuple of lat and lon

def get_cur_weather(lat, lon, API_KEY):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric').json()
    data = WeatherData(
        main= resp.get('weather')[0].get('main'),
        description= resp.get('weather')[0].get('description'),
        icon= resp.get('weather')[0].get('icon'),
        temperature= resp.get('main').get('temp') #no '[0]' as it does not return a dictionary but instead a list
    )

    return data

def get_country_code(countryName):
    countryName = ' '.join(countryName.split()) 
    country = pycountry.countries.get(name=countryName)
    if country is None:
        # fuzzy search fallback handles "South Korea" vs "Korea, Republic of" 
        results = pycountry.countries.search_fuzzy(countryName)
        country = results[0]
    return country.alpha_2  # e.g. 'NZ'

def main(cityName, countryName):
    countryCode = get_country_code(countryName)
    lat,lon = get_lat_lon(cityName,countryCode, api_key)
    weather_data = get_cur_weather(lat, lon, api_key)
    return weather_data

#if __name__ == '__main__':
  #  lat,lon = get_lat_lon({cityName},'NZ', api_key)
   # print(get_cur_weather(lat, lon, api_key))

