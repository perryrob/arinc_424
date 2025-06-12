# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES
from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from geo_json.geometry import true_course_deg, distance_deg
from math import fabs, sqrt
import collections
import heapq

from route.graph import Fix, Edge

from dijkstar import Graph, find_path

class Route:
    def __init__(self, conn, DEP_edge, DES_edge,
                 fuel_duration,
                 max_alt,
                 AIRWAY_TYPES,
                 cruise_alt,
                 cruise_speed,
                 wind=None,
                 edges=None):

        self.edges = edges
        self.cost = None
        self.conn=conn
        self.DEP_edge = DEP_edge
        self.DES_edge = DES_edge
        self.limit_duration = True
        if fuel_duration > 40:
            self.limit_duration = False
        self.fuel_duration=fuel_duration
        self.max_alt = max_alt
        self.AIRWAY_TYPES=AIRWAY_TYPES
        self.cruise_alt = cruise_alt
        self.cruise_speed = cruise_speed
        self.wind=wind

        if self.edges is None:
            self.get_no_wind_route()
        
    def get_wind_route(self):

        intermediate_duration = 0
        fuel_stops = []
        
        if self.wind is None:
            for edge in self.edges:
                intermediate_duration += edge.distance
                if intermediate_duration >= self.fuel_duration:
                    intermediate_duration = 0
                    fuel_stops.append(Fix(0,
                                          'Fuel Stop',
                                          edge.fix1.point[0],
                                          edge.fix1.point[1],{}))

                intermediate_duration = 0

                
        else:
            for i in range(0,len(self.edges)):
                edge = self.edges[i]
                # Calling get_nav with a wind populates the edge
                # with all of the requied nav data.
                COG,HEAD,SOG,TEMP,ETE = edge.get_nav(self.wind,
                                                     self.cruise_speed,
                                                     self.cruise_alt)
                if  self.limit_duration: # Duration is distance
                    intermediate_duration += ETE
                else:
                    intermediate_duration += edge.distance
                    
                if intermediate_duration >= self.fuel_duration:  
                    intermediate_duration = 0
                    fuel_stops.append(Fix(0,
                                          'Fuel Stop',
                                          edge.fix1.point[0],
                                          edge.fix1.point[1],{}))

        return (self.edges, self.cost, fuel_stops)
        
    def get_no_wind_route(self):

        direct_edge = Edge(self.DEP_edge.fix1, self.DES_edge.fix1, 'direct')

        # Westbound course 181-360
        sql = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_SQL]
        values = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_VALUES]

        cursor = self.conn.cursor()
        cursor.execute( sql )

        airways = cursor.fetchall()
        cursor.close()

        fix_map = {}
        id_name_map = {}
        airway_fixes = []
    
        # Initialize the "direct" portion of the lookup table
        id_name_map[self.DEP_edge.fix1.id] = self.DEP_edge.fix1
        id_name_map[self.DES_edge.fix1.id] = self.DES_edge.fix1

        fix_map[self.DEP_edge.fix1.fix_id] = self.DEP_edge.fix1
        fix_map[self.DES_edge.fix1.fix_id] = self.DES_edge.fix1

        graph = Graph(undirected=True)
    
        for fix in airways:

            id = fix[values['id']]
            route_id = fix[values['route_id']]
            fix_id = fix[values['fix_id']]
            sequence = fix[values['sequence']]
            longitude = fix[values['longitude']]
            latitude  = fix[values['latitude']]
            mea = fix[values['mea']]
            distance = fix[values['distance']]
        
            # Description codes of EE,NE,VE indicate end of routes
            description_code = fix[values['description_code']].strip()

            # Filter out the airways not requested by the user. Jet
            # routes is an example.
            if route_id[0] not in self.AIRWAY_TYPES:
                continue

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
                
                if mea is not None and mea > self.max_alt: continue
                
                edge = Edge(fix_1,fix_2,route_id)
                edge = Edge(fix_2,fix_1,route_id)


                ############################################################
                #
                # Hey, if the wind object is not none use ETE as the
                # cost function.
                #
                if self.wind is not None:
                    try:
                        COG,HEAD,SOG,TEMP,ETE = edge.get_nav(self.wind,
                                                             self.cruise_speed,
                                                             self.cruise_alt)
                        graph.add_edge( fix_1.id, fix_2.id,
                                        ETE)

                    except Exception as e:
                        # Edge is outside of weather coverage.
                        continue

                else:
                    graph.add_edge( fix_1.id, fix_2.id,
                                    edge.get_distance())
            
            # Clear the prevoius route and start a new one.
            if description_code in ['EE','NE','VE']:
                airway_fixes.clear()


        # Add the small direct portion of the airports to the first
        # fix to the graph

        graph.add_edge( fix_map[self.DEP_edge.fix1.fix_id].id,
                        fix_map[self.DEP_edge.fix2.fix_id].id,
                        self.DEP_edge.get_distance())
    
        graph.add_edge( fix_map[self.DES_edge.fix1.fix_id].id,
                        fix_map[self.DES_edge.fix2.fix_id].id,
                        self.DES_edge.get_distance())
    
        path_info = find_path(graph,
                              self.DEP_edge.fix1.id,
                              self.DES_edge.fix1.id)

        self.edges = []
        
        for idx in range(1,len(path_info.nodes)):

            fix1 = id_name_map[path_info.nodes[idx-1]]
            fix2 = id_name_map[path_info.nodes[idx]]
           
            distance = path_info.costs[idx-1]
            route_str=''
            
            if fix2.get_edges() is not None:
                for edge in fix2.get_edges():
                    if fix1 in edge and fix2 in edge:
                        route_str =  edge.name
                        route_str = route_str + \
                            '(mea '+ str(fix2.attrs['mea']) +  ')' 
                if route_str == '':
                    route_str='direct'
            
            fix1.clear_edges()
            fix2.clear_edges()
            
            edge = Edge(fix1,fix2,route_str)
            
            self.edges.append(  edge )

        self.cost = path_info.total_cost

        return (self.edges, self.cost)
    
    def format_430(self):
        intermediate_distance = 0
        ret_val=''
        next_edge = None
        total_distance = 0.0
        fix_dis = 0
        total_time=0

        ############################################################
        #
        # Starting with the departure fix I can taverse the edges
        # until get_edges returns a None
        #
        fix1 = self.DEP_edge.fix1
        des_edge = None
        while True:
            fix2 = fix1.get_edges()[0].fix2

            dep_edge=fix1.get_edges()[0]
            
            if fix2.get_edges() is None:
                if des_edge is None:
                    fix1.add_edge( Edge(fix1,fix2,'direct') )
                else:
                    fix1.add_edge( Edge(fix1,fix2,des_edge.name) )
                break # We've reached the route's end

            des_edge=fix2.get_edges()[0]
            
            if dep_edge.is_colinear(des_edge):
                fix1.clear_edges()
                fix1.add_edge( Edge(fix1,des_edge.fix2,des_edge.name) )
            fix1 = fix2

        
        ############################################################
        #
        # Test iterated list
        self.edges.clear()
        self.cost = 0
        fix1 = self.DEP_edge.fix1
        while True:
            edge = fix1.get_edges()[0]
            self.cost += edge.distance
            self.edges.append(edge)
            fix2 = edge.fix2
            if fix2.get_edges() is None: break # We've reached the route's end
            fix1 = fix2

    def __str__(self):
        ret_val=''
        total_time=0
        intermediate_duration = 0
        
        for i in range(0,len(self.edges)):
            edge = self.edges[i]
            if i == 0:                
                ret_val += str(edge.fix1) + '\n'
            ret_val += '\t'+edge.name+\
                '|{:3.1f} nm|'.format(edge.distance)+\
                '{:3.0f} deg'.format(edge.crs)

            if self.limit_duration:
                if edge.has_nav:
                    intermediate_duration += edge.ETE
            else:
                intermediate_duration += edge.distance
            
            if edge.has_nav:
                ret_val+='|{:3.0f} ktas'.format(edge.SOG)
                ret_val+='|{:3.0f} min|\n'.format(edge.ETE*60.0)
                total_time+=edge.ETE
            else:
                ret_val += '\n'

            if intermediate_duration >= self.fuel_duration:
                if self.limit_duration:
                    ret_val += '\n------------------------------- Fuel @ ' + \
                        str(self.fuel_duration) + \
                        ' time: {:2.1f} hrs\n'.format(intermediate_duration)

                else:
                    ret_val += '\n------------------------------- Fuel @ ' + \
                        str(self.fuel_duration) + \
                        ' dis: ' + str(intermediate_duration) +'nm\n'
                intermediate_duration = 0

            ret_val+= str(edge.fix2) + '\n'
        ret_val+='-----------------------------\n'
        if edge.has_nav:
            ret_val+='Total Distance: {:4.1f} nm | {:2.1f} hrs | {:4.1f} ktas\n'.format(self.cost,total_time,self.cost/total_time)
        else:
            ret_val+='Total Distance: {:4.1f}\n'.format(self.cost)
        return ret_val
        
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
    
    direct_edge = edges[0]
    to_crs = direct_edge.crs
    from_crs = direct_edge.recip()

    # print(dep_fix,dest_fix) # Fix objects
    
    # Find the closest waypoint
    sql = FEATURE_SQL_QUERIES['ALL_WAYPOINTS'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['ALL_WAYPOINTS'][FEATURE_VALUES]

    cursor = conn.cursor()
    cursor.execute( sql )

    wpts = cursor.fetchall()
    cursor.close()

    end_points = [fix_points[0],fix_points[1]]
    closest_edges = [None,None]


    # direct_edge = Edge(self.DEP_edge.fix1, self.DES_edge.fix1, 'direct')
    
    # Loop through all the waypoints and find the closest one to the departure
    # point. I need to extend this and take into acount where the departure
    # point starts and the destination point ends. I need to find the closest
    # point from the direction for the departure point.

    OFF_COURSE=30
    des_list=[]
    dep_list=[]
    
    for wpt in wpts:

        if wpt[values['route_id']][0] not in AIRWAY_TYPES: continue
        
        p_fix = Fix(wpt[values['id']],
                    wpt[values['name']],
                    wpt[values['longitude']],wpt[values['latitude']],
                    {'mea':0})



        dep_edge = Edge( end_points[0], p_fix, 'direct')
        des_edge = Edge( end_points[1], p_fix, 'direct')

        dep_list.append(dep_edge)
        des_list.append(des_edge)

    # Now sort by distance.
    dep_list.sort(key=lambda x: x.distance)
    des_list.sort(key=lambda x: x.distance)

    ret_val = [None,None]

    # Sort through the sorted closest waypoints from the
    # departure and destination airports
    for edge in dep_list[:20]:
        if ret_val[0] is None:
            ret_val[0] = edge
        elif fabs(ret_val[0].crs-to_crs) > fabs(edge.crs-to_crs):
            ret_val[0] = edge

    for edge in des_list[:20]:
        if ret_val[1] is None:
            ret_val[1] = edge
        elif fabs(ret_val[1].crs-from_crs) > fabs(edge.crs-from_crs):
            ret_val[1] = edge

    return (ret_val[0],ret_val[1])
