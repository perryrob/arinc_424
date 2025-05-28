# A little snippet so I can run test cases.
# e.g. python3 app/weather/stations.py
if __name__ == '__main__':
    import sys
    sys.path.append("app")

import json

from weather.json_to_sql import JSON_SQL
from weather.feature_sql import FEATURE_SQL_QUERIES
from weather.feature_sql import FEATURE_SQL,FEATURE_VALUES

from route.graph import Fix, Edge

from weather.gzip_cache import GzipCache

from scipy.spatial import Delaunay
from collections import UserList

class Station(UserList):


    def __init__(self, xy=[] ):
        super().__init__(xy)
        
    def init_from_json(self, json_data={}):
        self.json_data = json_data
        self.station = 'FAA'
        if 'lon' in self.json_data.keys() and \
           'lat' in self.json_data.keys():
            self.vertex = (float(self.json_data['lon']),
                           float(self.json_data['lat']))
        else:
            self.station = 'METEO'
            location=self.json_data['location']
            self.vertex = (float(location['longitude']),
                           float(location['latitude']))

        self.__init__(self.vertex)
        
    def is_faa(self):
        return self.station == 'FAA'

    def x(self):
        return self[0]
    def y(self):
        return self[1]
    
    def get_vertex(self):
        return self.vertex
    
    def get(self, k):
        return self.json_data[k]
    
    def __str__(self):
        return str(self.json_data)

class Stations:
    # use_stations is a filter list of stations. None is use all
    DATA_URL='https://aviationweather.gov/data/cache/stations.cache.json.gz'
    # DATA_URL='https://bulk.meteostat.net/v2/stations/lite.json.gz'
    LOCAL_FILE='app/aviation_weather/stations.json'
    def __init__(
            self, conn,
            remote_file=DATA_URL,
            local_file=LOCAL_FILE, persist=False, filter_list=[]
    ):

        zc = GzipCache(remote_file,local_file)
        jsql=JSON_SQL('station',zc.get_data())

        json_data = zc.get_json_data()

        self.stations = []
        self.station_by_icaoid = {}

        index=0

        for jd in json_data:
            s = Station()
            s.init_from_json(jd)
            # If a filter list was sent in use it to shorten the list
            found_station=False
            for k in ['icaoId','iataId','faaId']:            
                if jd[k] in filter_list:
                    found_station=True
                    break

            if not found_station: continue
            
            self.stations.append(s)
            self.station_by_icaoid[k]=int(index)
            index = index + 1           


        # Traingulate the station list.
        self.delaunay_triangles = Delaunay(self.stations)

        
        if persist:        
            try:
                cursor = conn.cursor()
                cursor.execute( jsql.table_drop_sql() )
                cursor.close()
                conn.commit()
            except:
                conn.rollback()

            cursor = conn.cursor()
            cursor.execute( jsql.table_create_sql() )
            cursor.close()
            conn.commit()

            cursor = conn.cursor()
            for insert in jsql.create_inserts():
                cursor.execute( insert )

            cursor.close()
            conn.commit()
            
    def get(self, id):
        retval = None
        try:
            retval = self.get_by_icao(id)            
        except:
            try:
                retval= self.get_by_icao('K'+id)
            except:
                try:
                    retval = self.stations.get_by_faa(id)
                except:
                    print('Could not find: ' + id)        
        return retval
    
    def get_by_icao(self,k):
        return self.stations[self.station_by_icaoid[k]]

    def get_by_faa(self,k):
        return self.stations[self.station_by_faaid[k]]

    def barycentric_weights(self,v,p):
        Wv1=((v[1].y()-v[2].y())*(p.x()-v[2].x()) +    \
             (v[2].x()-v[1].x())*(p.y()-v[2].y())) /   \
             ((v[1].y()-v[2].y())*(v[0].x()-v[2].x())+ \
              (v[2].x()-v[1].x())*(v[0].y()-v[2].y()))
        
        Wv2=((v[2].y()-v[0].y())*(p.x()-v[2].x()) +    \
             (v[0].x()-v[2].x())*(p.y()-v[2].y())) /   \
             ((v[1].y()-v[2].y())*(v[0].x()-v[2].x())+ \
              (v[2].x()-v[1].x())*(v[0].y()-v[2].y()))
        
        Wv3=1-Wv1-Wv2

        return (Wv1,Wv2,Wv3)
    
    def get_barycetric_for_point(self,
                                 yp=(-110.35797222222222,31.999444444444446)):
        
        tri_idx = self.delaunay_triangles.find_simplex(yp)

        if tri_idx == -1: raise Exception("Point is outside of station triangulation")
            
        stations=[
            self.stations[i] for i in self.delaunay_triangles.simplices[tri_idx]
        ]
        weights = self.barycentric_weights(stations,Station(yp))
        return (stations,weights)
        
if __name__ == '__main__':
    s=Stations(None)
    print(s.get_by_icao('KTUS'))
