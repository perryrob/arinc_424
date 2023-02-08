# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES

from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data

from geo_json.geometry import true_course_deg, distance_deg

from math import fabs

def distance_crs( conn, fixes ):

    '''
    Assume VORs are 3 letters airports 4 letters and waypoints 5 leters
    '''

    points = []
    
    for fix in fixes[0]:
        sql = None
        values = None
        wp = None
        TABLES = ['VORS','AIRPORTS','WAYPOINTS']

        for table in TABLES:
            cursor = conn.cursor()
            
            sql = FEATURE_SQL_QUERIES[table][FEATURE_SQL]
            sql=sql%fix
            values = FEATURE_SQL_QUERIES[table][FEATURE_VALUES]
            
            cursor.execute( sql )
            wp = cursor.fetchone()
            if wp is None:
                continue
            else:
                break
            cursor.close()

        if wp is None:
             print( fix, ' does not exist..')
             return []
        points.append( [wp[values['name']],
                       (wp[values['longitude']],
                        wp[values['latitude']])]
                      )
        points[0].append(' ---')
        points[0].append('  ---')
        for ii in range(1,len(points)):
            crs = true_course_deg(points[ii-1][1],points[ii][1], True )
            dis = distance_deg( points[ii-1][1], points[ii][1] )
            points[ii].append('{:3.1f}'.format(crs))
            points[ii].append('{:4.2f}'.format(dis))
            
    return points

def proposed_route( conn, dep='KTUS', dest='KMYF', AIRWAY_TYPES=['V','T','J'] ):

    dep_pt,dest_pt = distance_crs( conn, [[dep,dest]] )

    # Find the closest VOR
    sql = FEATURE_SQL_QUERIES['ALL_VORS'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['ALL_VORS'][FEATURE_VALUES]

    cursor = conn.cursor()
    cursor.execute( sql )

    vors = cursor.fetchall()
    cursor.close()
    
    # ( departure, destination )
    points = [ (dep_pt[1][0],dep_pt[1][1]),               
               (dest_pt[1][0],dest_pt[1][1])]
    closest_vors = [None,None]
    # Loop through all the VORs and find the closest one to the departure
    # point
    for vor in vors:
            p2 = ( vor[values['longitude']],vor[values['latitude']])
            name = vor[values['name']]            
            declination = vor[values['declination']]
            if len(name) != 3: continue            
            for i in range(0,2):                
                dis = distance_deg(points[i],p2)
                # Gotta be a plain old VOR if there are 3 chars
                if closest_vors[i] is None :
                    closest_vors[i] = (
                        name , dis, float(dest_pt[2]) + declination
                    )
                else:
                    if closest_vors[i][1] > dis:
                        closest_vors[i] = (
                            name, dis, float(dest_pt[2]) + declination
                        )
                
    graph_list = {}
    print( closest_vors )
    return fix_airways( conn, closest_vors[0][0],closest_vors[1][0], 
                        AIRWAY_TYPES, graph_list , None )

def fix_airways( conn, FIX, DEST_FIX, AIRWAY_TYPES, graph_list,
                 ROUTE_ID ):

    sql = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_VALUES]

    if ROUTE_ID is None:
        sql = sql%(FIX,'XXXX')
    else:
        sql = sql%(FIX,ROUTE_ID)

    cursor = conn.cursor()
    cursor.execute( sql )

    airways = cursor.fetchall()
    cursor.close()

    fix_sequences=[ (a[values['sequence']],a[values['route_id']])
                    for a in airways ]

               
    for fix_sequence,route_id in fix_sequences:
        for direction in [('<=','BCK'), ('>=','FWD')]:

            sql = FEATURE_SQL_QUERIES['AIRWAY_SEQ'][FEATURE_SQL]
            values = FEATURE_SQL_QUERIES['AIRWAY_SEQ'][FEATURE_VALUES]
            sql = sql%(FIX,direction[0],fix_sequence)
    
            cursor = conn.cursor()
            cursor.execute( sql )

            fixes = cursor.fetchall()
            cursor.close()

            for fix in fixes:
               fix_airways( conn, fix[values['fix_id']],
                            DEST_FIX,
                            AIRWAY_TYPES, graph_list,
                            route_id )
               print(direction,fix)
