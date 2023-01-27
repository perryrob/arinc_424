
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
    'WAYPOINTS':('''select  longitude, latitude,waypoint_id from waypoint''',{
        'longitude':0,
        'latitude':1,
        'name':2,
    }),
    'AIRWAYS':('''select A.route_id, A.sequence, A.longitude, A.latitude,A.fix_section_code,A.fix_subsection_code,A.outbound_mag_course,A.inbound_mag_course from airway A where A.fix_section_code is not NULL and A.fix_subsection_code is not NULL order by A.route_id,A.sequence''',{
        'name':0,
        'sequence':1,
        'longitude':2,
        'latitude':3,
        'fix_section_code':4,
        'fix_subsection_code':5,
        'outbound_course':6,
        'inbound_course':6
    })
}
