# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES
from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from geo_json.geometry import true_course_deg, distance_deg
from math import fabs, sqrt
import collections
import heapq

from route.graph import Fix, Edge

from dijkstar import Graph, find_path

def line_distance(f1,f2,f0):

    p1 = f1.rad_points()
    p2 = f2.rad_points()
    p0 = f0.rad_points()

    A = p0[0] - p1[0]
    B = p0[1] - p1[1]
    C = p2[0] - p1[0]
    D = p2[1] - p1[1]

    dot = A*C + B*D
    len_sq = C*C + D*D
    # param > 0 and param <=1 point is perp to line segement
    # param < 0 closest point is P! beyond line segment
    # param > 1 closest point is P2 beyond line segment
    param = -1
    on_line = False
    if len_sq !=0:
        param = fabs(dot / len_sq)

    err = 0.001
        
    if param > 1 + err:
        xx = p2[0]
        yy = p2[1]
    else:
        on_line=True
        xx = p1[0] + param * C
        yy = p1[1] + param * D

    dx = p0[0] - xx
    dy = p0[1] - yy

        
    return (sqrt(dx**2 + dy**2), on_line)

def distance_crs( conn, fixes ):

    '''
    Assume VORs are 3 letters airports 4 letters and waypoints 5 leters
    '''
    fix_points = []

    idx=0
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
        
        # small values of idx should not conflict with unique DB ids
        fix_points.append( Fix(idx, wp[values['name']],
                               wp[values['longitude']],
                               wp[values['latitude']],
                               {'mea':0}
                               )
                          )
        idx=idx+1
    edges = []
    for i in range(1,len(fix_points)):
        edges.append(Edge( fix_points[i-1], fix_points[i], 'direct' ))

    return edges,fix_points

def closest_wpts( conn, dep='KTUS', dest='KMYF', AIRWAY_TYPES=['V','T','J'] ):

    edges,fix_points = distance_crs( conn, [[dep,dest]] )

    # print(dep_fix,dest_fix) # Fix objects
    
    # Find the closest VOR
    sql = FEATURE_SQL_QUERIES['ALL_WAYPOINTS'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['ALL_WAYPOINTS'][FEATURE_VALUES]

    cursor = conn.cursor()
    cursor.execute( sql )

    wpts = cursor.fetchall()
    cursor.close()

    end_points = [fix_points[0],fix_points[1]]
    closest_edges = [None,None]

    # Loop through all the waypoints and find the closest one to the departure
    # point. I need to extend this and take into acount of where the departure
    # point starts and the destination point ends. I need to find the closest
    # point from the direction for the departure point.
    for wpt in wpts:

        if wpt[values['route_id']][0] not in AIRWAY_TYPES: continue
        
        p_fix = Fix(wpt[values['id']],
                    wpt[values['name']],
                    wpt[values['longitude']],wpt[values['latitude']],
                    {'mea':0})
        
        
        for i in range(0,2):

            dis,on_line = line_distance( end_points[0], 
                                         end_points[1],
                                         p_fix )
            
            edge = Edge( end_points[i], p_fix, 'direct')
            if closest_edges[i] is None :
                closest_edges[i] = edge
            else:
                if closest_edges[i].get_distance() > edge.get_distance() and \
                   on_line:
                    closest_edges[i] = edge
                 
    return closest_edges

def find_route( conn, DEP_edge, DES_edge, AIRWAY_TYPES, max_alt=18000 ):

    sql = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_VALUES]
    
    cursor = conn.cursor()
    cursor.execute( sql )

    airways = cursor.fetchall()
    cursor.close()

    fix_map = {}
    id_name_map = {}
    airway_fixes = []
    
    # Initialize the "direct" portion of the lookup table
    id_name_map[DEP_edge.fix1.id] = DEP_edge.fix1
    id_name_map[DES_edge.fix1.id] = DES_edge.fix1
    fix_map[DEP_edge.fix1.fix_id] = DEP_edge.fix1
    fix_map[DES_edge.fix1.fix_id] = DES_edge.fix1

    graph = Graph(undirected=True)
    
    for fix in airways:

        id = fix[values['id']]
        route_id = fix[values['route_id']]
        fix_id = fix[values['fix_id']]
        sequence = fix[values['sequence']]
        longitude = fix[values['longitude']]
        latitude  = fix[values['latitude']]
        mea = fix[values['mea']]
        
        # Description codes of EE,NE,VE indicate end of routes
        description_code = fix[values['description_code']].strip()
        
        if route_id[0] not in AIRWAY_TYPES:
            continue

        # if mea is not None and mea > max_alt:
        #    continue

        fix_node = None
        
        if fix_id in fix_map.keys():
            fix_node = fix_map[fix_id]
            if fix_node.attrs['mea'] is None and mea is not None:
                fix_node.attrs['mea'] = mea
        else:
            fix_node = Fix(
                id, fix_id, longitude, latitude, {'mea':mea}
            )
            fix_map[fix_id] = fix_node
            id_name_map[id] = fix_node
            
        airway_fixes.append(fix_node)
        
        if len(airway_fixes) >= 2:
            fix_1 = airway_fixes[-2]
            fix_2 = airway_fixes[-1]
            edge = Edge(fix_1,fix_2,route_id)

            if mea is not None and mea > max_alt: continue

            graph.add_edge( fix_1.id, fix_2.id,
                            edge.get_distance())
            
        # Clear the prevoius route and start a new one.
        if description_code in ['EE','NE','VE']:
            airway_fixes.clear()


    # Add the small direct portion of the airports to the first
    # fix to the graph

    graph.add_edge( fix_map[DEP_edge.fix1.fix_id].id,
                    fix_map[DEP_edge.fix2.fix_id].id,
                    DEP_edge.get_distance())
    
    graph.add_edge( fix_map[DES_edge.fix1.fix_id].id,
                    fix_map[DES_edge.fix2.fix_id].id,
                    DES_edge.get_distance())
    
    path_info = find_path(graph,
                          DEP_edge.fix1.id,
                          DES_edge.fix1.id)

    ret_val = []

    for idx in range(1,len(path_info.nodes)):
        fix1 = id_name_map[path_info.nodes[idx-1]]
        fix2 = id_name_map[path_info.nodes[idx]]
        route_str=''
        distance = path_info.costs[idx-1]
        for edge in fix2.get_edges():
            if fix1 in edge and fix2 in edge:
                route_str = route_str + edge.name
                route_str = route_str + '(mea '+ str(fix2.attrs['mea']) +  ')-' 
            elif idx == 1: # This may be a hack, investigate later.
                route_str='direct '

        route_str = route_str[:-1]

        fix1.clear_edges()
        fix2.clear_edges()
        edge = Edge(fix1,fix2,route_str)
        ret_val.append(  edge )

    return (ret_val,path_info.total_cost)


