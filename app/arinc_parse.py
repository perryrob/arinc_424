from parser.Parser import RecordParser
from translator import Translators

from translator.Translators import FIELD_REFERENCES
from spec.arinc_424_18_parser import ARINC_424_PARSE_DEF

from db.DB_Manager import DB_ARINC_Tables, DB_connect, DB_ARINC_data

ARINC424_INPUT_FILE='cifp/FAACIFP18'
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
    ('P','D'), # SID
    ('P','E'), # STAR
    ('P','F'), # Approaches
    ('P','G'), # Runways
    ('P','I'), # Localizer
    ('P','N'), # Terminal Navaid
    ('P','P'), # Path Point
    ('P','S'), # MSA
    ('U','C'), # CLASS B,C and D Airsapce
    ('U','R'), # Special Use Airspace    
]

supported = SUPPORTED

parser = RecordParser( ARINC424_INPUT_FILE, supported, STATS, Translators )
parsed_record_dict = parser.get_records()

#for record_key in supported:
#    print(parsed_record_dict[record_key])


db_tables = DB_ARINC_Tables( supported, ARINC_424_PARSE_DEF, FIELD_REFERENCES)

create_statements = db_tables.table_create_sql()
drop_statements = db_tables.table_drop_sql()


db_connect = DB_connect()


for statement in drop_statements:
    try:
        db_connect.exec( statement )        
    except Exception as e:
        pass

for statement in create_statements:
    db_connect.exec( statement,False )


arinc_data = DB_ARINC_data( supported, ARINC_424_PARSE_DEF, parsed_record_dict )
insert_arinc_data_list = arinc_data.create_inserts()

for insert in insert_arinc_data_list:
    db_connect.exec( insert, False )

db_connect.commit()
db_connect.close()