# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES
from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from geo_json.geometry import true_course_deg, distance_deg
from math import fabs
import collections
import heapq


Fix = collections.namedtuple('Fix','id route_id fix_id distance')
Route   = collections.namedtuple('Route'  , 'distance path')

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

    neighbors = collections.defaultdict(set)

    origin_fix=None
    destination_fix = None

    graph = Graph()

    departure_fixes = []
    destination_fixes = []
    
    for fix in airways:
        
        if fix[values['route_id']][0] not in AIRWAY_TYPES:
            continue

        airway_fix = Fix( fix[values['id']],
                          fix[values['route_id']],
                          fix[values['fix_id']],
                          fix[values['distance']])
        DEBUG=False
        if airway_fix.route_id == 'V66':
            DEBUG=True

        if DEBUG:
            print( airway_fix.fix_id)
        
        if fix[values['fix_id']] == DEP_VOR:
            departure_fixes.append(airway_fix)

        if fix[values['fix_id']] == DEST_VOR:
            destination_fixes.append(airway_fix)

        if fix[values['distance']] is None:
            # This is the end of the airway
            graph.connect(origin_fix,
                          Fix( fix[values['id']],
                               fix[values['route_id']],
                               fix[values['fix_id']],
                               0)
                          )
            destination_fix = None
            origin_fix = None
            continue
        
        if origin_fix is None:
            origin_fix = airway_fix
            continue
        
        if destination_fix is None:
            destination_fix = airway_fix
            graph.connect(origin_fix,destination_fix)
            origin_fix = destination_fix
            destination_fix = None


    distance,path =  graph.dijkstra( departure_fixes, destination_fixes )
    print('==================================================================')
    for fix in path:
        print(fix)
