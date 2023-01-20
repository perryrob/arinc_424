

POST_CREATE_SQL=[
    ('Link up airways and waypoints',
    'update airway A set waypoint_id = ( select id from waypoint B where A.fix_id = B.waypoint_id );'),
    
    ('Link up airways with VORs',
    'update airway A set vor_id = ( select id from vor B where A.fix_id = B.VOR_id );'),
    
    ('Link up the runways',
     'update runway R set airport_fid = (select id from airport A where A.airport_id = R.airport_id);'),

    ('Link up the runway localizers',
    'update localizer L set runway_fid = (select id from runway R where R.airport_id = L.airport_id and L.runway_id = R.runway_id);'),

    ('Link up the airport NDBs',
    'update airport_ndb N set airport_fid = (select id from airport A where N.airport_id = A.airport_id);'),

    ('Link up the MSA',
    'update airport_msa M set airport_fid = (select id from airport A where A.airport_id = M.airport_id);')


    
]
