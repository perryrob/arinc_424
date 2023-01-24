
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
    'AIRWAYS':('''select route_id, sequence, longitude, latitude from airway order by route_id,sequence''',{
        'name':0,
        'sequence':1,
        'longitude':2,
        'latitude':3
    })
}
