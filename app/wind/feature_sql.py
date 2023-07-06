
FEATURE_SQL=0
FEATURE_VALUES=1

FEATURE_SQL_QUERIES={
    'VORS': ('''select DME_longitude,DME_latitude,longitude,latitude from vor where vor_id  = '%s' ''',{
        'longitude':0,
        'latitude':1,
        'lon':2,
        'lat':3,
        }),
        'AIRPORT': ('''select longitude,latitude from airport where name like '*%s' ''',{
        'longitude':0,
        'latitude':1,
        })

}
