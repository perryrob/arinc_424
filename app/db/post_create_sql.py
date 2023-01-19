

POST_CREATE_SQL=[

    # One to many airport waypoint table
    'create table OTM_AIRPORT_WAYPOINT('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_waypoint_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_waypoint_id foreign key(airport_waypoint_id) '+\
    'references airport_waypoint(id) '+\
    'on delete set null);',

    # One to many airport SID table
    'create table OTM_AIRPORT_SID('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_sid_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_sid_id foreign key(airport_sid_id) '+\
    'references sid(id) '+\
    'on delete set null);',

    # One to many airport STAR table
    'create table OTM_AIRPORT_STAR('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_star_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_star_id foreign key(airport_star_id) '+\
    'references star(id) '+\
    'on delete set null);',

    # One to many airport Approach table
    'create table OTM_AIRPORT_APPROACH('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_approach_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_approach_id foreign key(airport_approach_id) '+\
    'references approach(id) '+\
    'on delete set null);',

    # One to many airport Runway table
    'create table OTM_AIRPORT_RUNWAY('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_runway_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_runway_id foreign key(airport_runway_id) '+\
    'references runway(id) '+\
    'on delete set null);',

    # One to many airport Runway table
    'create table OTM_AIRPORT_LOCALIZER('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_localizer_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_localizer_id foreign key(airport_localizer_id) '+\
    'references localizer(id) '+\
    'on delete set null);',

    # One to many airport NAVaid table
    'create table OTM_AIRPORT_NAVAID('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_navaid_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_navaid_id foreign key(airport_navaid_id) '+\
    'references airport_navaid(id) '+\
    'on delete set null);',

    # One to many airport MSA table
    'create table OTM_AIRPORT_MSA('+\
    'id serial primary key, '+\
    'airport_id integer, '+\
    'airport_msa_id integer, '+\
    'constraint airport_id foreign key(airport_id) '+\
    'references airport(id) '+\
    'on delete set null, '+\
    'constraint airport_msa_id foreign key(airport_msa_id) '+\
    'references airport_msa(id) '+\
    'on delete set null);',

    # Link up airways and waypoints
    'update airway A set waypoint_id = ( select id from waypoint B where A.fix_id = B.waypoint_id );',
    # Link up airways with VORs
    'update airway A set vor_id = ( select id from vor B where A.fix_id = B.VOR_id );'
]
