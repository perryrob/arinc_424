
FEATURE_SQL=0
FEATURE_VALUES=1

FEATURE_SQL_QUERIES={
    'STATION': ('''select lon,lat from station where faaid  = '%s' ''',{
        'longitude':0,
        'latitude':1,
        'lon':0,
        'lat':1,
        }),
    'VORS': ('''select vor_id,longitude,latitude from VOR''',{
        'vor_id':0,
        'longitude':1,
        'latitude':2,
        }),
}
