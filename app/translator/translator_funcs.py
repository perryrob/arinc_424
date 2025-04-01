from datetime import datetime, timedelta

from exceptions.CIFPExceptions import InvalidFloatFormat,InvalidIntegerFormat

SECTION_SUBSECTION = [None,None]


def noop(arg):
    return arg

def func52(arg): # record_type
    switch={
        'S':'STD',
        'T':'TAILORED',
    }
    return switch.get(arg,'UNK /' + arg)

def func53(arg):
    return arg.strip()

def func54( arg ):
    global SECTION_SUBSECTION
    if SECTION_SUBSECTION[0] is None:
        SECTION_SUBSECTION[0]=arg
    return arg

def func55( arg ):
    global SECTION_SUBSECTION
    if SECTION_SUBSECTION[1] is None:
        SECTION_SUBSECTION[1]=arg
    return arg


def func56(arg):
    return arg.strip()

def func57(arg):
    switch={
        'ER':        
        {
            'A' :'Airline',
            'C': 'Control',
            'D': 'Direct',
            'H': 'Helicopter',
            'O': 'Official',
            'R': 'RNAV',
            'S': 'Unassigned'
        },
        'PD':
        {
            '0': 'Engine Out',
            '1': 'Runway Transition',
            '2': 'Common Route',
            '3': 'Enroute Tranistion',
            '4': 'RNAV Runway Transition',
            '5': 'RNAV Common Route',
            '6': 'RNAV Enroute Transition',
            'F': 'FMS Runway Transition',
            'M': 'FMS Common Route',
            'S': 'FMS Enroute Transition',
            'T': 'VECTOR Runway Transition',
            'V': 'VECTOR Enroute Transition',
        },
        'PE':
        {
            '1': 'Enroute Transition',
            '2': 'Common Route',
            '3': 'Runway Tranistion',
            '4': 'RNAV Enroute Transition',
            '5': 'RNAV Common Route',
            '6': 'RNAV Runway Transition',
            '7': 'Profile Decsent Enroute Transition',
            '8': 'Profile Decsent Common Transition',
            '8': 'Profile Decsent Runway Transition',
            'F': 'FMS Enroute Transition',
            'M': 'FMS Common Route',
            'S': 'FMS Runway Transition'

        },
        'PF':
        {
            'A' : 'Transition',
            'B' : 'Backcourse',
            'D' : 'VOR/DME',
            'F' : 'FMS',
            'G' : 'IGS',
            'I' : 'ILS',
            'J' : 'GNSS',
            'L' : 'Localizer',
            'M' : 'MLS',
            'N' : 'NDB',
            'P' : 'GPS',
            'Q' : 'NDB DME',
            'R' : 'RNAV',
            'S' : 'VOR ARC',
            'T' : 'TACAN',
            'V' : 'VOR',
            'W' : 'MLS A',
            'X' : 'LDA',
            'Y' : 'MLS B C',
            'Z' : 'Missed'
        },
    }
    return switch.get(SECTION_SUBSECTION[0]+\
                      SECTION_SUBSECTION[1],{}).get(arg,'UNK' + '/' + arg)


def func58(arg):
    return arg.strip()

def func59(arg):
    return arg.strip()

def func510(arg):
    typ = func58(arg[0:1])
    rwy = arg[1:3]
    desig = arg[3:4]
    mult = arg[4:5]
    ret_val = typ + ' ' + rwy + ' ' + desig + ' ' + mult
    return ret_val.strip()

def func510(arg):
    return arg.strip()

def func511(arg):
    return arg.strip()

def func512(arg):
    return arg.strip()

def func513(arg):
    return arg.strip()

def func514(arg):
    return arg.strip()

def func515(arg):
    return arg.strip()

def func516(arg):
    # Data can be bad for this spec
    if arg == 'O': arg = '0'
    return int(arg.strip())

def func517(arg):
    return arg

def func518(arg):
    return arg.strip()

def func519(arg):
    return arg.strip()

def func520(arg):
    return arg.strip()

def func521(arg):
    return arg.strip()

def func522(arg):
    return arg.strip()

def func522(arg):
    return arg.strip()

def func523(arg):
    return arg.strip()

def func524(arg):
    try:
        base = float(arg[0:3])
        tenths = float(arg[3:4]) / 10
        return base + tenths
    except:
        raise InvalidFloatFormat('func524')

def func525(arg):
    return func524(arg)

def func526(arg):
    return func524(arg)

def func527(arg):
    try:
        base = float(arg[0:3])
        tenths = float(arg[3:4]) / 10
        return base + tenths
    except:
        raise InvalidFloatFormat('func527')

def func528(arg):
    return arg.strip()

def func529(arg):
    return arg.strip()

def func530(arg):
    try:
        return int(arg)
    except:
        raise InvalidIntegerFormat('func530')


def func531(arg):
    try:
        return int(arg)
    except:
        raise InvalidIntegerFormat('func531')

def func533(arg):
    return arg.strip()

def func534( arg ):
    
    try:
        global SECTION_SUBSECTION

        if 'D' in SECTION_SUBSECTION and ' '  in SECTION_SUBSECTION:
            base = arg[0:3]
            dec = arg[3:5]
        else:
            base = arg[0:4]
            dec = arg[4:5]

        return float(base + '.'+dec)
    except:
        raise InvalidFloatFormat('func535', {'arg':arg} )

def func535( arg ):
    '''
    Used On: Navaid Records (VHF, NDB and
    Airport/Heliport
    Localizer/Markers/Locators)
    Length: 5 characters (including "blanks")
    Character Type: Alpha
    '''
    switch=[{'V': 'VOR'},
            {'D': 'DME',
             'T': 'TACAN 17,59, 70-169',
             'M' : 'MIL TACAN 1-16,60-69',
             'I': 'ILS/DME ILS/TACAN',
             'N': 'MLS/DME/N',
             'P':'MLS/DME/P'},
            {'T': 'Terminal',
             'L': 'Low Altitude',
             'H': 'High Altitude',
             'U': 'UND',
             'C': 'ILS/TACAN'},
             {'D': 'BIASED ILSDME or ILSTACAN',
              'A': 'Automatic Transcribed Weather Broadcast',
              'B': 'Scheduled Weather Broadcast',
              'W':'No Voice',
              ' ': 'Voice'},
            {' ': 'Colocated Navaids',
             'N': 'Non-Collocated Navaids'}
            ]
    ret_val = []
    for i in range(0,5):
        ret_val.append(switch[i].get(arg[i],'UNK'+'/'+arg[i]))
    return ret_val

def func536( arg ):
    # N 32 05 5497
    try:
        ns = arg[0:1]
        if ns == 'S':
            ns = -1.0
        else:
            ns = 1.0
            
        degs = float(arg[1:3])
        mins = float(arg[3:5]) / 60.0
        secs = arg[5:7]
        dsecs = arg[7:9]
        secs = float(secs+'.'+dsecs) / 3600.0
        return ns * (degs + mins + secs)
    except:
        raise InvalidFloatFormat('func530')


def func537( arg ):
    try:
        ew = arg[0:1]
        if ew == 'W':
            ew = -1.0
        else:
            ew = 1.0
            
        degs = float(arg[1:4])
        mins = float(arg[4:6]) / 60.0
        secs = arg[6:8]
        dsecs = arg[8:9]
        secs = float(secs+'.'+dsecs) / 3600.0
        return ew * (degs + mins + secs)
    except:
        return None


def func539(arg):
    try:
        ew = arg[0:1]
        if ew == 'W':
            ew = -1.0
        elif ew == 'E':
            ew = 1.0
        elif ew == 'T':
            return 0
            
        degs = float(arg[1:4])
        tenths = float(arg[4:5]) / 10
        return ew * (degs + tenths)
    except:
        return None

    
def func538(arg):
    return arg.strip()

def func540( arg ):
    try:
        return float(arg)
    except:
        return None

def func541(arg):
    return arg.strip()    
    
def func542(arg):
    switch=[
        {'C': 'Combined Named Intersection and RNAV',
         'I' : 'Unnamed, Chart Intersection',
         'N' : 'NDB Navaid as Waypoint',
         'R' : 'Named Intersection',
         'U' : 'Uncharted Airway Intersection',
         'V' : 'VFR Waypoint',
         'W' : 'RNAV Waypoint'},
        {'A' : 'Final Approach Fix',
         'B' : 'Initial and Final Approach Fix',
         'C' : 'Final Approach Course Fix',
         'D' : 'Intermediate Approach Fix',
         'E' : 'Off-Route intersection in the FAA National Reference System',
         'F' : 'Off Route Intersection',
         'I' : 'Initial Approach Fix',
         'K' : 'Final Approach Course Fixat Initial Approach Fix',
         'L' : 'Final Approach Course at Intermediate Approach Fix',
         'M' : 'Missed Approach Fix',
         'N' : 'Initial Approach Fix and Missed Approach FIx',
         'O' : 'Oceanic Entry/Exit Waypoint',
         'P' : 'Pitch and Catch Point in the FAA High Altitude Redesign',
         'S' : 'AACAA and SUA Waypoints in FAA High Altitude Redesign',
         'U' : 'FIR/UIR or Controoled Airspace Intersection',
         'V' : 'Latitude/Longitude Intersection, Full Degree of Latitude',
         'W' : 'Latitude/Longitude Intersection, Half Degree of Latitude',
         ' ' : ''},
        {' ': ''}
        ]
    ret_val = []
    for i in range(0,3):
        ret_val.append(switch[i].get(arg[i],'UNK'+'/'+arg[i]))
    return ret_val

def func543(arg):
    return arg.strip()

def func544(arg):
    return arg.strip()

def func545(arg):
    try:
        ret_val = float(arg[0:3]) + float(arg[3:4]) / 10.0
        return ret_val
    except:
        return None

def func546(arg):
    return arg.strip()

def func547(arg):
    return arg.strip()

def func548(arg):
    return func531(arg)

def func549(arg):
    return arg.strip()

def func550(arg):
    return func531(arg)

def func551(arg):
    try:
        deg = float(arg[0:1])
        huns = float(arg[1:3])
        return  deg+huns
    except:
        return None

def func552(arg):
    return func551(arg)
    
def func553(arg):
    try:
        return int(arg)
    except:
        return None
    
def func554(arg):
    return func553(arg)

def func555(arg):
    return func553(arg)

def func556(arg):
    return arg.strip()

def func557(arg):
    return func553(arg)

def func571(arg):
    return arg.strip()

def func5197(arg):
    switch={'NAR' :'North American 1983 GRS 80'}
    return switch.get(arg,'UNK' + '/' + arg)

def func532( arg ):
    yr = int('20' + arg[0:2])
    days = 28 * int(arg[2:4])
    d = datetime(yr,1,1) + timedelta( days-1)
    
    # Reset the Section and Subsection becuase this is the end of the data line
    global SECTION_SUBSECTION
    SECTION_SUBSECTION=[None,None]
    return d.strftime('%m/%d/%Y')
               
def func566( arg ):
    try:
        ewt = arg[0:1]
        if ewt == 'E':
            ewt = -1.0
        elif ewt == 'W':
            ewt = 1.0
        else:
            return 0.0
        deg = float(arg[1:4])
        tens = float(arg[4:5]) / 10.0
        return ewt * ( deg + tens )
    except:
        return None

def func5170(arg):
    return arg.strip()

def func5158(arg):
    return arg.strip()

            
def ndb_class( arg ):
    switch=[
        {'H': 'NDB',
         'S':' SABH',
         'M': 'Marine Beacon'},
        {'I': 'Inner Marker',
         'M': 'Middle marker',
         'O': 'Outer Marker',
         'C': 'Back Marker'},
        {'H': '200 Watts or More',
         ' ': '50 - 1999 Watts',
         'M': '25 to less than 50 Watts',
         'L': 'Less than 25 Watts'},
        {'A': 'Automatic Weather',
         'B': 'Scheduled Weather',
         'W': 'No Voice',
         ' ': 'Voice'},
        {'B': 'BFO Ops'}
        ]
    ret_val = []
    for i in range(0,5):
        ret_val.append(switch[i].get(arg[i],'UNK'+'/'+arg[i]))
    return ret_val

def apt_ndb_class( arg ):
    switch=[
        {'H': 'NDB',
         'S':' SABH',
         'M': 'Marine Beacon'},
        {'I': 'Inner Marker',
         'M': 'Middle marker',
         'O': 'Outer Marker',
         'C': 'Back Marker'},
        {'H': '200 Watts or More',
         ' ': '50 - 1999 Watts',
         'M': '25 to less than 50 Watts',
         'L': 'Less than 25 Watts'},
        {'A': 'Automatic Weather',
         'B': 'Scheduled Weather',
         'W': 'No Voice',
         ' ': 'Voice'},
        {'B': 'BFO Ops',
         'A': 'Locator/Marker Collocated',
         'N': 'Locator/Middle Marker not collocated'}
        ]
    ret_val = []
    for i in range(0,5):
        ret_val.append(switch[i].get(arg[i],'UNK'+'/'+arg[i]))
    return ret_val

def waypoint_description(arg):
    switch=[
        {'A' : 'Airport as Waypoint',
         'E' : 'Essential Waypoint',
         'F' : 'Off Airway Waypoint',
         'G' : 'Runway/Helipad as Waypoint',
         'H' : 'Heliport as Waypoint',
         'N' : 'NDB as Waypoint',
         'P' : 'Phantom Waypoint',
         'R' : 'Non Essential Waypoint',
         'T' : 'Transition Essential Waypoint',
         'V' : 'VHF Navaid as Waypoint',
         ' ' : ''},
        {'B' : 'Flyover Waypoint, End of SID.STAR, Route, Final',
         'E' : 'End of Route',
         'U' : 'Uncharted Intersection',
         'Y' : 'Flyover Waypoint',
         ' ' : ''},
        {'A' : 'Unnamed Stepdown Fix After Final Approach Fix',
         'B' : 'Unnamed Stepdown Fix Before Final Approach Fix',
         'C' : 'ATC Compulsory Waypoint',
         'G' : 'Oceanic Waypoint',
         'M' : 'First Leg of Missed Approach Procedure',
         'P' : 'Path Point Fix',
         'S' : 'Named Stepdown Fix',
         ' ' : ''},
        {'A' : 'Initial Approach Fix',
         'B' : 'Intermediate Approach Fix',
         'C' : 'Initial Approach Fix with Hold',
         'D' : 'Initial Approach Fix with Final Approach Course Fix',
         'E' : 'Final End Point Fix',
         'F' : 'Published Final Approach Fix or DB Final Approach Fix',
         'H' : 'Holding Fix',
         'I' : 'Final Approach Course Fix',
         'M' : 'Published Missed Approach Fix',
         ' ' : ''}
        ]
    ret_val = []
    for i in range(0,4):
        ret_val.append(switch[i].get(arg[i],'UNK'+'/'+arg[i]))
    return ret_val

def waypoint_usage(arg):
    switch=[
        {' ' :'',
         'R' : 'RNAV'},
        {'B' : 'HI and LO Altitude',
         'H' : 'HI Altitude',
         'L' : 'LO Altitude',
         ' ' : 'Terminal Use Only'
         }]
    ret_val = []
    for i in range(0,2):
        ret_val.append(switch[i].get(arg[i],'UNK'+'/'+arg[i]))
    return ret_val

def route_type(arg):
    switch={'A':'Airline Airway',
            'C':'Control',
            'D': 'Direct Route',
            'H': 'Helicopter Airway',
            'O': 'Official Airway',
            'R': 'RNAV Airway',
            'S': 'Undesignated ATS Route'
            }
    return switch.get(arg,'UNK'+'/' + arg)

def route_level(arg):
    switch={
        'B' : 'HI and LO Altitude',
        'H' : 'HI Altitude',
        'L' : 'LO Altitude'}
    return switch.get(arg,'UNK'+'/' + arg)

def route_direction(arg):
    switch={
        ' ' : 'Bi-Directional',
        'F' : 'Forward',
        'B' : 'Back'}
    return switch.get(arg,'UNK'+'/' + arg)

def cruise_table_ind(arg):
    switch={'AA': 'ICAO Standard cruise table',
            'AO': 'Exception to ICAO Standard cruise table'}

    return switch.get(arg,'UNK'+'/' + arg)


def three_float_last_tenth(arg):
    try:
        ret_val = float(arg[0:2]) + float(arg[2:3]) / 10.0
        return ret_val
    except:
        return -1.0

    
def mag_course( arg ):
    try:
        ret_val = float(arg[0:3]) + float(arg[3:4]) / 10.0
        return ret_val
    except:
        return 'Possible True(T) Entry'

def route_distance( arg ):
    try:
         ret_val = float(arg[0:3]) + float(arg[3:4]) / 10.0
         return ret_val
    except:
        return 'Possible Holding Time (T) Entry'
