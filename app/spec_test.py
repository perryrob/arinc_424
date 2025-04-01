from spec.arinc_424_23_parser import ARINC_424_PARSE_DEF

KEYS=['D']

SUB_KEYS=[' ','B']

FORMAT_STR='%15s %25s %10s'

for k in KEYS:
    print(FORMAT_STR % ('Column','Field Name (Length)','Reference'))
    record = ARINC_424_PARSE_DEF[k]
    for sk in SUB_KEYS:
        pos=1
        for field in record[sk][1:]:
            # Create the Field position description the 'thru' text is added if
            # the field length is greater than 1
            field_str=''
            if field[1] == 1:
                field_str = str(pos)
            else:
                field_str = str(pos) +' - '  + str(pos+field[1]-1)
                
            pos = pos+field[1]
                
            print(FORMAT_STR % (field_str,field[0],field[2]))
        print('------------------------------------------------------------')
