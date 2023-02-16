
FEATURE_SQL=0
FEATURE_VALUES=1

FEATURE_SQL_QUERIES={
    'VORS': ('''select DME_longitude,DME_latitude,vor_id,frequency,declination from vor where DME_longitude is not NULL and vor_id = '%s' ''',{
        'longitude':0,
        'latitude':1,
        'name':2,
        'frequency':3,
        'declination':4,
        'elevation':5
        }),
    'WAYPOINTS':('''select  longitude, latitude,waypoint_id,type from waypoint where waypoint_id = '%s' ''',{
        'longitude':0,
        'latitude':1,
        'name':2,
        'type':3
    }),
    'AIRPORTS':('''select R.runway_id,R.runway_length,R.runway_magnetic_bearing,R.latitude,R.longitude,R.runway_gradient,R.landing_threshold_elevation,R.displaced_threshold_distance,R.runway_width,R.runway_description,A.airport_id,A.airport_reference_pt_latitude,A.airport_reference_pt_longitude,A.ifr_capability,A.magnetic_variation,A.airport_elevation from runway R join airport A on R.airport_fid=A.id where A.airport_id = '%s' ''',{
        'r_id':0,
        'r_length':1,
        'r_magnetic_bearing':2,
        'r_latitude':3,
        'r_longitude':4,
        'r_gradiant':5,
        'r_elevation':6,
        'r_displaced_distance':7,
        'r_width':8,
        'r_description':9,
        'name':10,
        'latitude':11,
        'longitude':12,
        'a_ifr':13,
        'a_mag_variation':14,
        'elevation':15,
    }),
    'ALL_VORS': ('''select DME_longitude,DME_latitude,vor_id,frequency,declination from vor where DME_longitude is not NULL and navaid_class like 'V%' ''',{
        'longitude':0,
        'latitude':1,
        'name':2,
        'frequency':3,
        'declination':4,
        'elevation':5
        }),
    'FIX_SEQUENCE':('''select id,route_id,fix_id,sequence,route_distance_from,longitude,latitude,description_code from airway  order by route_id,sequence''',{
        'id':0,
        'route_id':1,
        'fix_id':2,
        'sequence':3,
        'distance':4,
        'longitude':5,
        'latitude':6,
        'description_code':7
    }),
}
