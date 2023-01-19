

POST_CREATE_SQL=[
    'update airway A set waypoint_id = ( select id from waypoint B where A.fix_id = B.waypoint_id );',
    'update airway A set vor_id = ( select id from vor B where A.fix_id = B.VOR_id );'
]
