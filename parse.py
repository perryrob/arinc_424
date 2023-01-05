
from Parser import RecordParser
import Translators

ARINC424_INPUT_FILE='/home/perryr/proj/cifp/cifp/FAACIFP18'
last_vhf = None
STATS={}

parser = RecordParser( ARINC424_INPUT_FILE, [], STATS, Translators )



for record in parser.get_records():
    print(record)

print( STATS )
