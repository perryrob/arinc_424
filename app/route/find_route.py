# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES
from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from geo_json.geometry import true_course_deg, distance_deg
from math import fabs
import collections
import heapq

from route.graph import Fix, Edge

from dijkstar import Graph, find_path


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
            p_vor = ( vor[values['longitude']],vor[values['latitude']])
            name = vor[values['name']]            
            declination = vor[values['declination']]
            # filter to take only 3 letter VORs
            if len(name) != 3: continue            
            for i in range(0,2):                
                dis = distance_deg(points[i],p_vor)

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

    return (closest_vors[0][0],closest_vors[1][0])

def find_airways( conn, DEP_fix, DES_fix, AIRWAY_TYPES ):

    sql = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_VALUES]

    cursor = conn.cursor()
    cursor.execute( sql )

    airways = cursor.fetchall()
    cursor.close()

    fix_map = {}
    name_id_map = {}

    # We need to make sure that we don't make duplicate fixes.
    # That makes assembling the graph harder

    airway_fixes = []

    graph = Graph(undirected=True)
    
    for fix in airways:

        id = fix[values['id']]
        route_id = fix[values['route_id']]
        fix_id = fix[values['fix_id']]
        sequence = fix[values['sequence']]
        longitude = fix[values['longitude']]
        latitude  = fix[values['latitude']]
        description_code = fix[values['description_code']].strip()

        # Description codes of EE,NE,VE indicate end of routes
        
        if route_id[0] not in AIRWAY_TYPES:
            continue

        fix_node = None
        
        if id in fix_map.keys():
            fix_node = fix_map[id]
        else:
            name_id_map[fix_id] = id
            fix_node = Fix(
                id, fix_id, longitude, latitude
            )
            fix_map[id] = fix_node

        airway_fixes.append(fix_node)
        
        if len(airway_fixes) >= 2:
            fix_1 = airway_fixes[-2]
            fix_2 = airway_fixes[-1]
            edge = Edge(fix_1,fix_2,route_id)
            graph.add_edge( fix_1.id, fix_2.id, edge.get_distance())
        # Clear the prevoius route and start a new one.
        if description_code in ['EE','NE','VE']:
            airway_fixes.clear()
        
    # Now I have the entire CIFP graph assembled.
    dep_fix = name_id_map[DEP_fix]
    des_fix = name_id_map[DES_fix]

    print( DEP_fix,'->',DES_fix)
    
    path_info = find_path(graph,dep_fix,des_fix)

    for node_id in path_info.nodes:
        print(fix_map[node_id])
    

    '''            
    for route in fix_routes[DEP_VOR]:
        print( route )
    
    for fix in fix_routes.keys():
        print(fix,fix_routes[fix])

    for route in route_fixes.keys():
        print(route,route_fixes[route])
    '''
    print('==================================================================')

