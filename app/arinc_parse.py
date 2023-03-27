from parser.Parser import RecordParser

import sys

from spec.arinc_424_18_parser import ARINC_424_PARSE_DEF

from db.DB_Manager import DB_ARINC_Tables, DB_connect, DB_ARINC_data

from db.post_create_sql import POST_CREATE_SQL

from CONFIG import ARINC424_INPUT_FILE,ARINC_DATA_FILE


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

def post_create_db( db_connect ):
    print('Running post create scripts to link up the foreign keys...')



