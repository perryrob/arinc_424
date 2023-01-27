

POST_CREATE_SQL=[
    ('Link up the runways',
     'update runway R set airport_fid = (select id from airport A where A.airport_id = R.airport_id);'),

    ('Link up the runway localizers',
    'update localizer L set runway_fid = (select id from runway R where R.airport_id = L.airport_id and L.runway_id = R.runway_id);'),

    ('Link up the airport NDBs',
    'update airport_ndb N set airport_fid = (select id from airport A where N.airport_id = A.airport_id);'),

    ('Link up the MSAs',
     'update airport_msa M set airport_fid = (select id from airport A where A.airport_id = M.airport_id);'),
    
    ('Link up airways to VORs',
     "update airway A set vor_id = (select id from vor V where vor_id = A.fix_id) where A.fix_section_code='D' and COALESCE(A.fix_subsection_code,'')='';"),
    
    ('Link up airways to NDBs',
     "update airway A set ndb_id = (select id from ndb B where ndb_id = A.fix_id and A.icao_region_code = B.ndb_icao_region) where A.fix_section_code='D' and A.fix_subsection_code = 'B';"),
    
    ('Link up airways to WAYPOINTSs',
     "update airway A set waypoint_id = (select id from waypoint W where waypoint_id = A.fix_id) where A.fix_section_code='E' and A.fix_subsection_code='A';"),

    ('AIRWAY Populate lon/lat from Waypoints',
     "update airway A set latitude = (select latitude from waypoint W where A.waypoint_id = W.id), longitude = (select longitude from waypoint W where A.waypoint_id = W.id), declination = (select dynamic_mag_variation from waypoint W where A.waypoint_id = W.id) where A.fix_section_code='E' and A.fix_subsection_code='A';"),

    ('AIRWAY Populate lon/lat from VOR DME position',
     "update airway A set latitude = (select latitude from vor V where A.vor_id = V.id), longitude = (select longitude from vor V where A.vor_id = V.id),declination = -(select declination from vor V where A.vor_id = V.id) where A.fix_section_code='D' and COALESCE(A.fix_subsection_code,'')='';"),

    
    ('AIRWAY Populate lat/lon from NDB',
     "update airway A set latitude = (select latitude from ndb N where A.ndb_id = N.id), longitude = (select longitude from ndb N where A.ndb_id = N.id), declination=(select variation from ndb N where A.ndb_id = N.id) where A.fix_section_code='D' and A.fix_subsection_code='B';"),

]
