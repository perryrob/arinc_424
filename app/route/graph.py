
from geo_json.geometry import distance_deg,true_course_deg

from math import fabs,pi

class Fix:
    def __init__(self, id, fix_id,
                 longitude,latitude,attrs):
        self.id = id
        self.fix_id = fix_id
        self.point = (longitude, latitude)
        self.edges = []
        self.attrs=attrs
        
    def get_edges(self):
        return self.edges
        
    def add_edge(self, edge):
        self.edges.append(edge)

    def clear_edges(self):
        self.edges.clear()

    def print_edges(self):
        for e in self.edges:
            print('-> ' +  str(e))

    def rad_points(self):
        return (self.point[0] * pi / 180.0,
                self.point[1] * pi / 180.0)

    def get_attrs(self):
        return self.attrs
    
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
        self.crs = true_course_deg(fix1.point,
                                   fix2.point )
        self.fix1.add_edge(self)
        self.fix2.add_edge(self)

        self.fixes = [fix1,fix2]

        
    def recip(self):
        if self.crs > 180.0:
            return self.crs -180
        return self.crs +180
    
    def get_distance(self):
        return self.distance

    def is_colinear(self,edge):
        # Make sure the edge has the same name
        name_is_same=False
        for route_id in self.name.split('-'):
            if route_id in edge.name.split('-'):
                name_is_same = True
                break
        
        if fabs(edge.crs - self.crs) <= 2.0 and name_is_same:
            return True
        elif fabs(edge.crs - self.recip()) <= 2.0 and name_is_same:
            return True
        
        return False
                    
    def get_neighbor(self,fix):
        if fix is self.fix2:
            return self.fix1
        return self.fix2

    def __iter__(self):
        yield from self.fixes
    
    def __str__(self):
        return str(self.fix1) + ' | ' + self.name + \
            ' | ' + str(self.distance) + ' | ' + str(self.fix2)

   
