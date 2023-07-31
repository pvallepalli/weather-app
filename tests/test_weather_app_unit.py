import unittest
from unittest.mock import patch, MagicMock
from app import app, get_weather

class TestWeatherAppUnit(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.requests.get')
    @patch('app.googlemaps.Client')
    def test_get_weather_valid_location(self, mock_gmaps_client, mock_requests_get):
        # Mock Google Maps Client and geocode response
        mock_geocode_response = [
            {'geometry': {'location': {'lat': 47.616787, 'lng': -122.210266}}}
        ]
        mock_gmaps_client.return_value.geocode.return_value = mock_geocode_response

        # Mock Open Meteo API response
        mock_api_response = {"latitude":47.616787,"longitude":-122.210266,"generationtime_ms":0.6029605865478516,"utc_offset_seconds":-25200,"timezone":"America/Los_Angeles","timezone_abbreviation":"PDT","elevation":27.0,"current_weather":{"temperature":74.3,"windspeed":4.2,"winddirection":295.0,"weathercode":0,"is_day":1,"time":"2023-07-30T15:00"},"daily_units":{"time":"iso8601","weathercode":"wmo code","temperature_2m_max":"°F","temperature_2m_min":"°F","sunrise":"iso8601","sunset":"iso8601","uv_index_max":""},"daily":{"time":["2023-07-30","2023-07-31","2023-08-01","2023-08-02","2023-08-03","2023-08-04","2023-08-05"],"weathercode":[3,3,0,0,3,3,0],"temperature_2m_max":[75.7,76.0,79.7,82.5,81.6,84.7,84.7],"temperature_2m_min":[58.8,55.6,55.2,55.4,57.2,59.0,59.9],"sunrise":["2023-07-30T05:44","2023-07-31T05:45","2023-08-01T05:46","2023-08-02T05:47","2023-08-03T05:49","2023-08-04T05:50","2023-08-05T05:51"],"sunset":["2023-07-30T20:46","2023-07-31T20:45","2023-08-01T20:43","2023-08-02T20:42","2023-08-03T20:40","2023-08-04T20:39","2023-08-05T20:37"],"uv_index_max":[7.10,7.05,7.10,7.05,7.10,6.75,6.75]}}
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = mock_api_response

        weather_data = get_weather("Bellevue, WA")
        self.assertIsNotNone(weather_data)
        self.assertIn('current_weather', weather_data)
        self.assertIn('daily_forecast', weather_data)

    @patch('app.googlemaps.Client')
    def test_get_weather_invalid_location(self, mock_gmaps_client):
        # Mock Google Maps Client and geocode response for invalid location
        mock_gmaps_client.return_value.geocode.return_value = []

        weather_data = get_weather("InvalidLocation")

        self.assertIsNone(weather_data)

if __name__ == '__main__':
    unittest.main()