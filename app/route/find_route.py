# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES
from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from geo_json.geometry import true_course_deg, distance_deg
from math import fabs
import collections
import heapq


from route.graph import RouteGraph


class Fix:
    def __init__(self, id, route_id, fix_id, sequence, distance,
                 longitude,latitude):
        self.id = id
        self.route_id = route_id
        self.fix_id = fix_id
        self.sequence = sequence
        self.distance = distance
        self.point = (longitude, latitude)
        self.neighbors = []
        self.routes = []
        
    def add_fix(self, fix):
        self.neighbors.append(fix)
        
    def add_route(self, route):
        self.routes.append(route)

class BiEdge:
    def __init__(self,name,node1,node2,distance):

        self.name = name

        node1.connect(node2)
        
        self.next_edge = None
        self.distance = distance

        
    def get_id_left(self):        
        return self.id_left

    def get_id_right(self):        
        return self.id_right

    def connect(self,edge):
        self.next_edge = edge
        edge.next_edge = self
    
class NodeFix:

    def __init__(self,name):
        self.name = name
        self.sibling = None
        
    def connect(self,node):
        self.sibling = node
        node.sibling = self
        
    def cost(self):
        return self.distance

        
class Heap(object):
    """A min-heap."""

    def __init__(self):
        self._values = []

    def push(self, value):
        """Push the value item onto the heap."""
        heapq.heappush(self._values, value)

    def pop(self):
        """ Pop and return the smallest item from the heap."""
        return heapq.heappop(self._values)

    def __len__(self):
        return len(self._values)

class Graph(object):
    """ A hash-table implementation of an undirected graph."""
    def __init__(self):
        # Map each node to a set of nodes connected to it
        self._neighbors = collections.defaultdict(set)

    def connect(self, node1, node2):
        self._neighbors[node1].add(node2)
        self._neighbors[node2].add(node1)

    def neighbors(self, node):
        yield from self._neighbors[node]

    def dijkstra(self, origins, destinations):
        """Use Dijkstra's algorithm to find the cheapest path."""

        routes = Heap()
        for origin in origins:
            for neighbor in self.neighbors(origin):
                distance = neighbor.distance
                routes.push(Route(distance=distance, path=[origin, neighbor]))
            visited = set()
            visited.add(origin)

        while routes:

            # Find the nearest yet-to-visit airport
            distance, path = routes.pop()
            fix = path[-1]
            if fix in visited:
                continue

            # We have arrived! Wo-hoo!
            if fix in  destinations:
                return distance, path

            # Tentative distances to all the unvisited neighbors
            for neighbor in self.neighbors(fix):
                if neighbor not in visited:
                    # Total spent so far plus the price of getting there
                    new_distance = distance + neighbor.distance
                    new_path  = path  + [neighbor]
                    routes.push(Route(new_distance, new_path))

            visited.add(fix)

        return float('infinity')



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

def find_airways( conn, DEP_VOR, DEST_VOR, AIRWAY_TYPES ):

    sql = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_SQL]
    values = FEATURE_SQL_QUERIES['FIX_SEQUENCE'][FEATURE_VALUES]

    cursor = conn.cursor()
    cursor.execute( sql )

    airways = cursor.fetchall()
    cursor.close()

    fix_routes={}
    route_fixes={}
    for fix in airways:

        id = fix[values['id']]
        route_id = fix[values['route_id']]
        fix_id = fix[values['fix_id']]
        sequence = fix[values['sequence']]
        distance = fix[values['distance']]
        longitude = fix[values['longitude']]
        latitude = fix[values['latitude']]
        
        if route_id[0] not in AIRWAY_TYPES:
            continue

        fix_tup = Fix(
            id, route_id, fix_id, sequence, distance, longitude, latitude )
        
        if fix_id in fix_routes.keys():
            fix_routes[fix_id].append(fix_tup)
        else:
            fix_routes[fix_id] = [ fix_tup ]

        if route_id in route_fixes.keys():
            route_fixes[route_id].append(fix_tup)
        else:
            route_fixes[route_id] = [ fix_tup ]
        

    route_graph = RouteGraph( fix_routes,route_fixes )
    route_graph.propose_route(DEP_VOR,DEST_VOR)
    '''            
    for route in fix_routes[DEP_VOR]:
        print( route )
    
    for fix in fix_routes.keys():
        print(fix,fix_routes[fix])

    for route in route_fixes.keys():
        print(route,route_fixes[route])
    '''
    print('==================================================================')

