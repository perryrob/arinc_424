
LAST_SECTION_CODE = None

def noop(arg):
    return arg

def strip(arg):
    return arg.strip()

def int_blank(arg):
    try:
        return int(arg)
    except:
        return arg

def section_code( arg ):
    switch={
        'A':'MORA',
        'D':'Navaid',
        'E':'Enroute',
        'H':'Heliport',
        'P':'Airport',
        'R':'Company Route',
        'T':'Tables',
        'U':'Airspace'
    }
    global LAST_SECTION_CODE
    LAST_SECTION_CODE = arg
    return switch.get(arg,'UNK')

def vfr_freq( arg ):
    return arg

def dec_latitude( arg ):
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
        return arg

def dec_longitude( arg ):
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
        return arg

def subsection_code( arg ):
    switch={ 'D':
             {
                 '': 'VHF Navaid',
                 'B':'NDB'
             }
    }
    return switch.get(LAST_SECTION_CODE,{}).get(arg,'UNK')

def vhf_freq( arg ):
    base = arg[0:3]
    dec = arg[3:5]
    return float(base + '.'+dec)

def elevation( arg ):
    try:
        return float(arg)
    except:
        return arg
    
def declination( arg ):
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
        return arg

def nav_class( arg ):
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

def waypoint_type(arg):
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
