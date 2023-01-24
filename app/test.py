
from geo_json.build_json import VOR,NDB, WAYPOINT, AIRWAY

from os import path

from geojson import FeatureCollection, dump
from geo_json.build_kml import kml_conversion

from db.DB_Manager import DB_connect
from db.feature_sql import FEATURE_SQL_QUERIES, FEATURE_SQL, FEATURE_VALUES

from CONFIG import ARINC_DATA_FILE

if __name__ == '__main__':

    db_connect = DB_connect()
    conn = db_connect.get_connection()
    cursor = conn.cursor()
    
    cursor.execute(FEATURE_SQL_QUERIES['VORS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['VORS'][FEATURE_VALUES]

    vors = cursor.fetchall()
    
    collection = []
    
    for vor in vors:
        
        center = (vor[feature_values['longitude']],
                      vor[feature_values['latitude']])
        collection.append(VOR(radius=2.5,
                              segments=36,
                              center=center,
                              variation=vor[feature_values['declination']],
                              properties={
                                  'name':vor[feature_values['name']],
                                  'frequency':vor[feature_values['frequency']]
                              }))

    cursor.close()

    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['NDBS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['NDBS'][FEATURE_VALUES]
                      
    ndbs = cursor.fetchall()

    for ndb in ndbs:
        center = (ndb[feature_values['longitude']],
                  ndb[feature_values['latitude']])

        collection.append(NDB(radius=1,
                              segments=20,
                              center=center,
                              properties={
                                  'name':ndb[feature_values['name']],
                                  'frequency':ndb[feature_values['frequency']]
                              }))

    cursor.close()
    
    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['WAYPOINTS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['WAYPOINTS'][FEATURE_VALUES]
                      
    wps = cursor.fetchall()

    for wp in wps:
        center = (wp[feature_values['longitude']],
                  wp[feature_values['latitude']])

        collection.append(WAYPOINT(radius=0.25,
                                   segments=3,
                                   center=center,
                                   properties={
                                       'name':wp[feature_values['name']],
                                   }))


    cursor.close()
    
    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['AIRWAYS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['AIRWAYS'][FEATURE_VALUES]
                      
    wps = cursor.fetchall()

    airways = {}
    
    for wp in wps:
        center = (wp[feature_values['longitude']],
                  wp[feature_values['latitude']])
        
        AIRWAY(airways,
               route_id = wp[feature_values['name']],
               center=center,
               properties={
                   'name':wp[feature_values['name']],
               })
    
    collection.append( AIRWAY( airways, None, None, None))
                        
    conn.commit()
    conn.close()
    
    f_collection = FeatureCollection(collection)

    kml = kml_conversion( f_collection )

    kml.save( path.join('/tmp','ARINC_DATA_FILE.kml') )
    
    with open(path.join('/tmp','ARINC_DATA_FILE.geojson'),'w') as f:
        dump(f_collection, f)
