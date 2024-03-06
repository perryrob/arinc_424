
import json


class Stations:
    def __init__(self,conn, input_file='app/aviation_weather/stations.cache.json'):
        with open( input_file, 'r') as f:
            txt = f.read()
            json_data = json.loads(txt)
            for station in json_data:
                print(station)
            
