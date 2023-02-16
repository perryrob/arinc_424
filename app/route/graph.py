
import heapq

from geo_json.geometry import distance_deg

class Fix:
    def __init__(self, id, fix_id,
                 longitude,latitude):
        self.id = id
        self.fix_id = fix_id
        self.point = (longitude, latitude)
        self.edges = []

    def get_edges(self):
        return self.edges
        
    def add_edge(self, edge):
        self.edges.append(edge)

    def print_edges(self):
        for e in self.edges:
            print('-> ' +  str(e))

    def __hash__(self):
        return hash(self.fix_id)

    def __eq__(self,other):
        if not isinstance(other,Fix): return False
        return self.id == other.id
    
    def __str__(self):
        return self.fix_id
    
class Edge:
    def __init__(self,fix1,fix2,name):
        self.fix1 = fix1
        self.fix2 = fix2
        self.name = name
        self.distance = distance_deg( fix1.point,
                                      fix2.point )
        self.fix1.add_edge(self)
        self.fix2.add_edge(self)
        
    def get_distance(self):
        return self.distance

    def get_neighbor(self,fix):
        if fix is self.fix2:
            return self.fix1
        return self.fix2
    
    def __str__(self):
        return str(self.fix1) + ' | ' + self.name + \
            ' | ' + str(self.distance) + ' | ' + str(self.fix2)

   
