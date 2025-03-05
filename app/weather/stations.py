import json

from weather.json_to_sql import JSON_SQL

from delaunay.quadedge.mesh import Mesh
from delaunay.quadedge.point import Vertex
from delaunay.delaunay import delaunay

class Stations:
    def __init__(self, conn, input_file='app/aviation_weather/stations.cache.json'):
        with open( input_file, 'r') as f:
            txt = f.read()
            
        jsql=JSON_SQL('station',txt)
        ############################################################
        #
        # Test the delaunay triangles
        #
        json_data = json.loads(txt)
        vertices = []
        for s in json_data:
            if float(s['lon']) > -127 and float(s['lat']) < 50 and \
               float(s['lon']) < -62 and float(s['lat']) > 16:
                # print( float(s['lon']),float(s['lat']) )
                vertices.append(Vertex(float(s['lon']),float(s['lat'])))

        m = Mesh()
        m.loadVertices(vertices)
        delaunay(m, 0, len(vertices)-1)


        lines = []
        for qe in m.quadEdges:
            if qe.org is not None:
                lines += [[[qe.org.x, qe.dest.x], [qe.org.y, qe.dest.y]]]
                # lines += [[[qe.org.x, qe.org.y], [qe.dest.x, qe.dest.y]]]

        for line in lines:
            print(line)

        # plotting, for example:
        '''
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        for line in lines:
            start, end = line

            ax.plot(start, end)

        plt.show()
        '''

        print(lines)
        # print(jsql.table_drop_sql())
        # print(jsql.table_create_sql())
        # print(jsql.create_inserts())
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
            
