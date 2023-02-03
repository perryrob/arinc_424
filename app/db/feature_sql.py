
FEATURE_SQL=0
FEATURE_VALUES=1

FEATURE_SQL_QUERIES={
    'VORS': ('''select DME_longitude,DME_latitude,vor_id,frequency,declination from vor where DME_longitude is not NULL and navaid_class like 'V%' ''',{
        'longitude':0,
        'latitude':1,
        'name':2,
        'frequency':3,
        'declination':4
        }),
    'NDBS':('''select longitude,latitude,ndb_id,frequency from ndb where longitude is not NULL''',{
        'longitude':0,
        'latitude':1,
        'name':2,
        'frequency':3,
        }),
    'WAYPOINTS':('''select  longitude, latitude,waypoint_id,type from waypoint''',{
        'longitude':0,
        'latitude':1,
        'name':2,
        'type':3
    }),
    'AIRWAYS':('''select A.route_id, A.sequence, A.longitude, A.latitude,A.fix_section_code,A.fix_subsection_code,A.outbound_mag_course,A.inbound_mag_course,A.description_code,A.minimum_altitude from airway A order by A.route_id,A.sequence''',{
        'name':0,
        'sequence':1,
        'longitude':2,
        'latitude':3,
        'fix_section_code':4,
        'fix_subsection_code':5,
        'outbound_course':6,
        'inbound_course':7,
        'description_code':8,
        'min_altitude':9
        
    }),
    'RUNWAYS':('''select R.runway_id,R.runway_length,R.runway_magnetic_bearing,R.latitude,R.longitude,R.runway_gradient,R.landing_threshold_elevation,R.displaced_threshold_distance,R.runway_width,R.runway_description,A.airport_id,A.airport_reference_pt_latitude,A.airport_reference_pt_longitude,A.ifr_capability,A.magnetic_variation,A.airport_elevation from runway R join airport A on R.airport_fid=A.id order by A.airport_id''',{
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
        'airport_id':10,
        'a_latitude':11,
        'a_longitude':12,
        'a_ifr':13,
        'a_mag_variation':14,
        'a_elevation':15,
    })
        
}
