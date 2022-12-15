
from Parser import RecordParser

ARINC424_INPUT_FILE='/home/perryr/proj/cifp/cifp/FAACIFP18'
last_vhf = None
STATS={}

parser = RecordParser( ARINC424_INPUT_FILE, [('D','')], STATS )



for record in parser.get_records():
    print(record)

print( STATS )
