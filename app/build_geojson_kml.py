
from geo_json.build_json import VOR,NDB, WAYPOINT, AIRWAY, RUNWAY
from geo_json.build_json import VOR_RADIUS,NDB_RADIUS, WAYPOINT_RADIUS 

from os import path

from geojson import FeatureCollection, dump
from geo_json.build_kml import kml_conversion, fly_to_camera

from db.DB_Manager import DB_connect
from db.feature_sql import FEATURE_SQL_QUERIES, FEATURE_SQL, FEATURE_VALUES

INCLUDE_AIRWAYS=['V','T','J']
INCLUDE_WAYPOINT_TYPES=['W  ','C  ','R  ','W  ']


def save_kmz(collection=[], file_name='UNK'):
    f_collection = FeatureCollection(collection)
    kml = kml_conversion( f_collection )
    print(file_name)
    kml.savekmz( file_name, format=False )


def fly_to( center=(0,0,0),roll=0,tilt=0,filename='fly_to.kmz'):
    kml = fly_to_camera( center=center,roll=roll,tilt=tilt )
    print(filename)
    kml.savekmz( filename, format=False )
    
if __name__ == '__main__':

    db_connect = DB_connect()
    conn = db_connect.get_connection()
    cursor = conn.cursor()

    print('Creta VOR json/kml')
    cursor.execute(FEATURE_SQL_QUERIES['VORS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['VORS'][FEATURE_VALUES]

    vors = cursor.fetchall()
    
    collection = []
    
    for vor in vors:
        
        center = (vor[feature_values['longitude']],
                      vor[feature_values['latitude']])
        collection.append(VOR(radius=VOR_RADIUS,
                              segments=36,
                              center=center,
                              variation=-vor[feature_values['declination']],
                              properties={
                                  'name':vor[feature_values['name']],
                                  'frequency':vor[feature_values['frequency']]
                              }))

    cursor.close()

    save_kmz(collection, 'ARINC_VOR.kmz')
    collection=[]
    
    print('Creta NDB json/kml')
    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['NDBS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['NDBS'][FEATURE_VALUES]
                      
    ndbs = cursor.fetchall()

    for ndb in ndbs:
        center = (ndb[feature_values['longitude']],
                  ndb[feature_values['latitude']])

        collection.append(NDB(radius=NDB_RADIUS,
                              segments=20,
                              center=center,
                              properties={
                                  'name':ndb[feature_values['name']],
                                  'frequency':ndb[feature_values['frequency']]
                              }))

    cursor.close()

    save_kmz(collection, 'ARINC_NDB.kmz')
    collection=[]

    print('Creta WAYPOINT json/kml')
    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['WAYPOINTS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['WAYPOINTS'][FEATURE_VALUES]
                      
    wps = cursor.fetchall()

    for wp in wps:
        # Filter Waypoints
        if wp[feature_values['type']] not in INCLUDE_WAYPOINT_TYPES:
              continue
        center = (wp[feature_values['longitude']],
                  wp[feature_values['latitude']])

        collection.append(WAYPOINT(radius=WAYPOINT_RADIUS,
                                   segments=3,
                                   center=center,
                                   properties={
                                       'name':wp[feature_values['name']],
                                   }))


    cursor.close()
    save_kmz(collection, 'ARINC_WAYPOINT.kmz')
    collection=[]
    
    print('Creta AIRWAY json/kml')
    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['AIRWAYS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['AIRWAYS'][FEATURE_VALUES]
                      
    wps = cursor.fetchall()

    airways = {}
    waypoint_types={}
    
    for wp in wps:
        name = wp[feature_values['name']]
        if name[0] not in INCLUDE_AIRWAYS:
            continue
        
        center = (wp[feature_values['longitude']],
                  wp[feature_values['latitude']])


        fix_section_subsection = wp[feature_values['fix_section_code']]+\
            wp[feature_values['fix_subsection_code']]
    
        properties = {
            'name':name,
            'description_code': wp[feature_values['description_code']],
            'SECTION_SUBSECTION': fix_section_subsection,
            'min_altitude': wp[feature_values['min_altitude']],
            'outbound_course': wp[feature_values['outbound_course']]
        }
        
        AIRWAY(airways,
               waypoint_types,
               route_id = name,
               center=center,
               properties=properties
               )
    
    collection.append( AIRWAY( airways, waypoint_types, None, None, None) )

    save_kmz(collection, 'ARINC_AIRWAY.kmz')
    collection=[]

    cursor.close()
    
    print('Creta RUNWAY json/kml')
    cursor = conn.cursor()
    cursor.execute(FEATURE_SQL_QUERIES['RUNWAYS'][FEATURE_SQL])
    feature_values = FEATURE_SQL_QUERIES['RUNWAYS'][FEATURE_VALUES]
                      
    rwys = cursor.fetchall()

    runways={}
    for rwy in rwys:
        airport_id = rwy[feature_values['airport_id']]
        center = (rwy[feature_values['a_longitude']],
                  rwy[feature_values['a_latitude']])
        
        runways = RUNWAY(runways , airport_id, rwy, feature_values )

    collection.append( RUNWAY(runways , None, None, feature_values=None ))

    save_kmz(collection, 'ARINC_RUNWAY.kmz')

    
    
    collection=[]
    conn.commit()
    conn.close()

    fly_to( center=(-110.9,32.1,36000),roll=0,tilt=0,filename='VIEW.kmz')

    
    # print('geojson')
    # with open('/tmp/ARINC_DATA_FILE.geojson','w') as f:
    #    dump(f_collection, f)
