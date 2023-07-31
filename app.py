import os
import requests
import googlemaps
from flask import Flask, render_template, request
import logging

app = Flask(__name__)
gmaps = googlemaps.Client(key=os.environ['GMAPS_API_KEY'])

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global recently_searched
recently_searched = []

def get_weather(location):
    logging.info(f"Getting weather data for location: {location}")
    try:
        # Fetch geographical coordinates (lat, lon) by using the location name
        geocode_result = gmaps.geocode(location)
        
        if len(geocode_result) > 0:
            lat, lon = geocode_result[0]['geometry']['location'].values()
            logging.info(f"Geographical coordinates for {location}: {lat}, {lon}")
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=auto"
            response = requests.get(api_url)
            if response.status_code == 200:
                weather_data = response.json()
                daily_forecast = []
                if 'daily' in weather_data:
                    for i in range(len(weather_data['daily']['time'])):
                        daily_forecast.append({
                            'date': weather_data['daily']['time'][i],
                            'max_temp': weather_data['daily']['temperature_2m_max'][i],
                            'min_temp': weather_data['daily']['temperature_2m_min'][i],
                            'uv_index': weather_data['daily']['uv_index_max'][i],
                            'sunrise': weather_data['daily']['sunrise'][i],
                            'sunset': weather_data['daily']['sunset'][i]
                        })
                    
                    # Append the recently searched location to the list
                    recently_searched.append(location)
                    # Keep only the last 5 recently searched locations
                    globals()["recently_searched"] = recently_searched[-5:]
                    
                    return {
                        'current_weather': weather_data['current_weather'],
                        'daily_forecast': daily_forecast
                    }
            else:
                logging.warning(f"Unable to fetch weather data for location: {location}. Status Code: {response.status_code}")
        else:
            logging.warning(f"Location not found: {location}")
            return None
    except Exception as e:
        logging.error(f"An error occurred while fetching weather data for location {location}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    location = request.form.get('location')
    weather_data = get_weather(location)
    return render_template('weather_result.html', location=location, weather_data=weather_data, recently_searched=recently_searched[::-1])

if __name__ == '__main__':
    logging.info("Weather App is starting...")
    app.run(debug=True)