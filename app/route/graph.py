
from geo_json.geometry import distance_deg,true_course_deg,deg_to_rad,rad_to_deg

from math import fabs,pi,sin,cos,asin,sqrt,fmod

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
        return (deg_to_rad(self.point[0]),
                deg_to_rad(self.point[1]))

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

        self.has_nav=False
        
        self.fix1 = fix1
        self.fix2 = fix2
        self.name = name
        self.distance = distance_deg( fix1.point,
                                      fix2.point )
        self.crs = true_course_deg(fix1.point,
                                   fix2.point, make_360=True)
        self.fix1.add_edge(self)
        self.fix2.add_edge(self)

        self.fixes = [fix1,fix2]
        self.mid_point = [(fix1.point[0]+fix2.point[0])/2,
                          (fix1.point[1]+fix2.point[1])/2]
    def recip(self):
        if self.crs > 180.0:
            return self.crs -180
        return self.crs +180

    def get_nav(self,wind,speed,alt):
        # COG = Course over ground
        # HEAD = Heading to offset wind
        # SOG = speed over ground
        # TEMP = Temperature at edge mid-point
        # ETE = estimated time enroute for the edge
        self.has_nav=True

        self.COG=None
        self.HEAD=None
        self.SOG=None
        self.TEMP=None
        self.ETE=None

        cruise_alt,wind_dir,wind_speed,temp =  wind.get_airdata_at_location(alt,
                                                                            self.mid_point)

        self.TEMP=temp
        SWC = wind_speed/speed*sin(deg_to_rad(wind_dir)/deg_to_rad(self.crs))
        if fabs(SWC) > 1:
            raise Exception('Cannot fly leg wind exceeds performance')

        self.HEAD = deg_to_rad(self.crs) + asin(SWC)
        self.HEAD = fmod(self.HEAD,2*pi)
        self.SOG = speed*sqrt(1-SWC**2)-\
            wind_speed*cos(deg_to_rad(wind_dir)-deg_to_rad(self.crs))
        if self.SOG <= 0:
            raise Exception('Cannot fly leg wind exceeds performance')
        
        # return (COG,HEAD,SOG,TEMP,ETE)
        self.HEAD=rad_to_deg(self.HEAD),
        self.ETE = self.distance/self.SOG
    
        return (self.crs,
                self.HEAD,
                self.SOG,
                self.TEMP,
                self.ETE)
    
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
            ' | ' + str(self.distance) + ' | ' + str(self.fix2) + \
            '|' + str(self.crs)

   
