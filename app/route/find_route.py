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

    dep_loc = (dep_pt[1][0],dep_pt[1][1])
    des_loc = (dest_pt[1][0],dest_pt[1][1])
    
    # Loop through all the VORs and find the closest one to the departure
    # point
    closest = None
    for vor in vors:
        p2 = ( vor[values['longitude']],vor[values['latitude']])
        name = vor[values['name']]
        dis = distance_deg(dep_loc,p2)
        declination = vor[values['declination']]
        if closest is None and len(name) ==3:
            closest = (name , dis, float(dest_pt[2]) + declination)
        else:
            if closest[1] > dis and len(name) ==3:
                closest = (name, dis, float(dest_pt[2]) + declination)

    cursor.close()
    graph_list = {}
    return fix_airways( conn, closest[0],
                        dep_loc, des_loc , AIRWAY_TYPES, graph_list )

def fix_airways( conn, fix, dep_pt, dest_pt, AIRWAY_TYPES, graph_list ):
    
    # Closest VOR 
    # print(closest) ('TUS', 1.8265092953374382, 267.3)
    # Now find the closest outbound traversal
    sql = FEATURE_SQL_QUERIES['FIX_AIRWAYS'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['FIX_AIRWAYS'][FEATURE_VALUES]
    sql = sql%fix
    
    cursor = conn.cursor()
    cursor.execute( sql )

    airways = cursor.fetchall()
    cursor.close()

    airway_list=[ a[values['name']] for a in airways ]
    
    # Start from the closest VOR and traverse all airways
    for airway_name in airway_list:

        # Airway filter like ignore J routes etc.
        if airway_name[0] not in  AIRWAY_TYPES:
            continue
        
        sql= FEATURE_SQL_QUERIES['ROUTE_AIRWAYS'][FEATURE_SQL]
        values = FEATURE_SQL_QUERIES['ROUTE_AIRWAYS'][FEATURE_VALUES]
        sql= sql%(airway_name)
        
        cursor = conn.cursor()
        cursor.execute( sql )

        airway = cursor.fetchall()

        fix_list=[ (a[values['id']],
                    a[values['fix_id']],a[values['sequence']],(
                        a[values['longitude']],
                        a[values['latitude']]
                    )
                    )
                   for a in airway ]
         
        p2 = (dest_pt[0],dest_pt[1])

        cursor.close()

        for id,fix,sequence,p1 in fix_list:
            dis = distance_deg(p1,p2)
            if airway_name in graph_list.keys():
                graph_list[airway_name].append(
                    [id,airway_name,fix,sequence,dis]
                )
            else:
                graph_list[airway_name] = [ [id,airway_name,fix,sequence,dis] ]


    return graph_list 
