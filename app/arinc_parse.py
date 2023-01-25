from parser.Parser import RecordParser
from translator import Translators

from translator.Translators import FIELD_REFERENCES

import sys

from spec.arinc_424_18_parser import ARINC_424_PARSE_DEF

from db.DB_Manager import DB_ARINC_Tables, DB_connect, DB_ARINC_data

from db.post_create_sql import POST_CREATE_SQL

from CONFIG import ARINC424_INPUT_FILE,ARINC_DATA_FILE

last_vhf = None
STATS={}

SUPPORTED=[
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

def cleanup_db(db_connect,db_tables):
    
    print('Cleaning up the old tables...')
    drop_statements = db_tables.table_drop_sql()
    for statement in drop_statements:
        try:
            db_connect.exec( statement )        
        except Exception as e:
            print('\t Ignored!')
            
def setup_db(db_connect,db_tables):

    print('Creating new empty tables...')
    create_statements = db_tables.table_create_sql()    
    for statement in create_statements:
        db_connect.exec( statement )


def parse( ARINC424_INPUT_FILE, supported, STATS, Translators):
    print('parsing the raw data....')
    parser = RecordParser( ARINC424_INPUT_FILE, supported, STATS, Translators )
    return  parser.get_records()

def load_db( db_connect, ARINC_424_PARSE_DEF, supported, parsed_record_dict):
    print('Building insert statements')
    arinc_data = DB_ARINC_data( supported, ARINC_424_PARSE_DEF,
                                parsed_record_dict )

    insert_arinc_data_list = arinc_data.create_inserts()

    print('Inserting data into the DB..')
    count=0
    for insert in insert_arinc_data_list:
        count = count + 1
        if divmod(count,10000)[1] == 0:
            print('<>',end='')
            sys.stdout.flush()
        try:        
            db_connect.exec( insert, False )
        except Exception as e:
            print('!',end='')
            sys.stdout.flush()
        
    print('!')
        
def post_create_db( db_connect ):
    print('Running post create sql to link up the foreign keys...')
    for msg,sql in POST_CREATE_SQL:
        print('\t' + msg)
        db_connect.exec( sql )

def close_db( db_connect ):
    print('Committing changes.') 
    db_connect.commit()
    db_connect.close()
    print('Database closed, success.')


if __name__ == '__main__':

    supported = SUPPORTED

    print('Building create  statements...')
    db_tables = DB_ARINC_Tables( supported, ARINC_424_PARSE_DEF,
                                 FIELD_REFERENCES)

    print('Connecting to the database')
    db_connect = DB_connect()

    cleanup_db(db_connect,db_tables)
    
    setup_db(db_connect,db_tables)
    
    parsed_record_dict = parse(ARINC424_INPUT_FILE, supported,
                               {}, Translators)
    
    
    load_db( db_connect, ARINC_424_PARSE_DEF, supported, parsed_record_dict)

    post_create_db( db_connect )

    close_db( db_connect )

