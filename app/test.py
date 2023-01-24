
from geo_json.build_json import VOR

from geojson import FeatureCollection, dump
from geo_json.build_kml import kml_conversion

from db.DB_Manager import DB_connect

if __name__ == '__main__':
    db_connect = DB_connect()
    conn = db_connect.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select DME_longitude,DME_latitude,vor_id,frequency,declination from vor where DME_longitude is not NULL and navaid_class like 'V%'
    ''')

    vors = cursor.fetchall()
    collection = []

    for vor in vors:
        
        center = (vor[0],vor[1])
        collection.append(VOR(radius=2.5,
                              segments=36,
                              center=center,
                              variation=vor[4],
                              properties={'name':vor[2],
                                          'frequency':vor[3]
                                          }))

    conn.commit()
    conn.close()
    
    f_collection = FeatureCollection(collection)

    kml = kml_conversion( f_collection )

    kml.save( '/tmp/test.kml')
    
    with open('/tmp/test.geojson','w') as f:
        dump(f_collection, f)
