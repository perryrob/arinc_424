
from build_geojson_kml import VOR_geom, NDB_geom, WAYPOINT_geom
from build_geojson_kml import AIRWAY_geom, AIRPORT_geom, fly_center

from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from db.post_create_sql import POST_CREATE_SQL

from translator.Translators import FIELD_REFERENCES
from spec.arinc_424_18_parser import ARINC_424_PARSE_DEF

from CONFIG import ARINC424_INPUT_FILE,ARINC_DATA_FILE

from arinc_parse import  cleanup_db,setup_db,parse,load_db,post_create_db

from translator import Translators
from translator.Translators import FIELD_REFERENCES


import argparse

SUPPORTED_SECTIONS_SUBSECTIONS=[
    ('A','S'), # MORA
    ('D',' '), # VOR
    ('D','B'), # NDB
    ('E','A'), # Waypoints
    ('E','R'), # Airways
    ('H','A'), # Helipads
    ('H','C'), # Terminal Waypoints
    ('H','F'), # Approaches
    ('H','S'), # MSA
    ('P','A'), # Airports
    ('P','G'), # Runways
    ('P','I'), # Localizer
    ('P','N'), # airport Navaid
    ('P','P'), # airport waypoint
    ('P','D'), # SID
    ('P','E'), # STAR
    ('P','F'), # Approaches
    ('P','S'), # MSA
    ('U','C'), # CLASS B,C and D Airsapce
    ('U','R'), # Special Use Airspace    
]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Write KMZ or json files generated from a parsed CIFP file.'
    )

    parser.add_argument('-c','--cifp',help='Input CIFP file.',
                        default='app/cifp/FAACIFP18')
    
    for val in ['vor','ndb','waypoint','airway','airport']:
        parser.add_argument('--'+val, help='create '+val+' KMZ and/or json file',
                        action='store_true')


    parser.add_argument('--clean_db',help='Purge all data and tabless. '+\
                        'then recreate db with blank schema.',action='store_true'
                        )

    parser.add_argument('--recreate_db',help='Purge all data and tabless. '+\
                        'then recreate db with blank schema.'+\
                        'parse CIFP file and load new data.',action='store_true'
                        )

    parser.add_argument('--fly_to', nargs=3, action='append', type=float,
                        metavar=('lon', 'lat', 'alt'),
                        help='Enter lon(deg) lat(deg) alt(m) for VIEW.kmz',
                        default=None
                        )
        
    args=parser.parse_args()

    conn = None
    db_connect = None
    try:
        db_connect = DB_connect()
        conn = db_connect.get_connection()
    except Exception as e:
        print('Unable to connect to the database...')
        raise(e)

    db_tables = DB_ARINC_Tables( SUPPORTED_SECTIONS_SUBSECTIONS,
                                 ARINC_424_PARSE_DEF,
                                 FIELD_REFERENCES)
    if args.clean_db:
        cleanup_db(db_connect,db_tables)
        setup_db(db_connect,db_tables)

    if args.recreate_db:
        cleanup_db(db_connect,db_tables)        
        setup_db(db_connect,db_tables)
        parsed_record_dict = parse(args.cifp,
                                   SUPPORTED_SECTIONS_SUBSECTIONS,
                                   {}, Translators)
    
    
        load_db( db_connect, ARINC_424_PARSE_DEF,
                 SUPPORTED_SECTIONS_SUBSECTIONS, parsed_record_dict)

        post_create_db( db_connect )
        conn.commit()
    
    if args.vor:
        VOR_geom(conn)

    if args.ndb:
        NDB_geom(conn)

    if args.waypoint:
        WAYPOINT_geom(conn)
        
    if args.airway:
        AIRWAY_geom(conn)
        
    if args.airport:
        AIRPORT_geom(conn)

    if  args.fly_to is not None:
        fly_center(args.fly_to[0])
        
    conn.commit()
    conn.close()
