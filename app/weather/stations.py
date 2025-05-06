# A little snippet so I can run test cases.
# e.g. python3 app/weather/stations.py
if __name__ == '__main__':
    import sys
    sys.path.append("app")

import json

from weather.json_to_sql import JSON_SQL
from weather.feature_sql import FEATURE_SQL_QUERIES
from weather.feature_sql import FEATURE_SQL,FEATURE_VALUES

from delaunay.quadedge.mesh import Mesh
from delaunay.quadedge.point import Vertex
from delaunay.delaunay import delaunay

from route.graph import Fix, Edge

from weather.gzip_cache import GzipCache

class Station:

    def __init__(self, json_data={}):
        self.json_data = json_data
        self.station = 'FAA'
        if 'lon' in self.json_data.keys() and \
           'lat' in self.json_data.keys():
            self.vertex = (Vertex(float(self.json_data['lon']),
                                  float(self.json_data['lat'])))
        else:
            self.station = 'METEO'
            location=self.json_data['location']
            self.vertex = (Vertex(float(location['longitude']),
                                  float(location['latitude'])))
    def is_faa(self):
        return self.station == 'FAA'
    
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
            local_file=LOCAL_FILE, persist=False
    ):

        zc = GzipCache(remote_file,local_file)
        jsql=JSON_SQL('station',zc.get_data())

        json_data = zc.get_json_data()

        self.stations = []
        self.station_by_icaoid = {}

        index=0

        for s in json_data:
            s = Station( s )
            self.stations.append(s)
            if s.is_faa():
                self.station_by_icaoid[s.get('icaoId')]=int(index)
            else:
                
                self.station_by_icaoid[s.get('identifiers')['icao']]=int(index)
            index = index + 1

            # self.mesh = Mesh()
            # self.mesh.loadVertices(vertices)
            # delaunay(self.mesh, 0, len(vertices)-1)
        
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

    def get_by_icao(self,k):
        return self.stations[self.station_by_icaoid[k]]
    def get_by_faa(self,k):
        return self.stations[self.station_by_faaid[k]]
    
    def get_delauney_edges(self):
        delauney_edges = []
        for qe in self.mesh.quadEdges:
            if qe.org is not None:
                # I should put the wind/temps in the None area for easy
                # retrieveal during interpolation
                f_org = Fix( qe.org.iataId,
                             qe.org.iataId,
                             qe.org.x, qe.org.y, None)
                
                f_dest = Fix( qe.dest.iataId,
                              qe.dest.iataId,
                              qe.dest.x, qe.dest.y, None)
                
                delauney_edges.append( Edge(
                    f_org,
                    f_dest,
                    qe.org.faaId+qe.dest.faaId
            ))
        return delauney_edges

        
if __name__ == '__main__':
    s=Stations(None)
    print(s.get_by_icao('KTUS'))
