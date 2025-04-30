# A little snippet so I can run test cases.
# e.g. python3 app/weather/stations.py
if __name__ == '__main__':
    import sys
    sys.path.append("app")

import json

from weather.json_to_sql import JSON_SQL

from delaunay.quadedge.mesh import Mesh
from delaunay.quadedge.point import Vertex
from delaunay.delaunay import delaunay

from route.graph import Fix, Edge

from io import BytesIO
import gzip
import requests

class GzipCache:
    def __init__(self,remote_file,local_file):
        response = requests.get(remote_file)
        self.unzipped_data = None
        if response.status_code == 200:
            with open(local_file, mode="wb") as of:
                of.write(response.content)            
        else:
            print('Could not update internet file.....')

        with gzip.open(local_file, 'rb') as inf:
            self.unzipped_data  = inf.read()

            
    def get_data(self):
        return self.unzipped_data

    def get_json_data(self):
        return json.loads(self.get_data())
 

                
class Stations:
    # use_stations is a filter list of stations. None is use all
    def __init__(self, conn,
                 remote_file='https://aviationweather.gov/data/cache/stations.cache.json.gz',
                 local_file='app/aviation_weather/stations.json',
                 use_stations=None):

        zc = GzipCache(remote_file,local_file)
        jsql=JSON_SQL('station',zc.get_data())

        json_data = zc.get_json_data()
        vertices = []

        for s in json_data:
            # {'icaoId': '32012', 'iataId': '-', 'faaId': '-', 'wmoId': '-', 'lat': 19.691, 'lon': -85.567, 'elev': 0, 'site': 'Woods Hole Stratus Wave Station', 'state': '--', 'country': '--', 'priority': 4}
            if s['iataId'] == '-': continue
            if use_stations is None or s['faaId'] in use_stations:
                v = (Vertex(float(s['lon']),float(s['lat'])))
                v.faaId = s['faaId']
                v.iataId = s['iataId']
                vertices.append(v)
                
                self.mesh = Mesh()
                self.mesh.loadVertices(vertices)
                delaunay(self.mesh, 0, len(vertices)-1)
       
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
    zc = GzipCache('https://aviationweather.gov/data/cache/stations.cache.json.gz',
             'app/aviation_weather/stations.json')
    print( zc.get_json_data() )
