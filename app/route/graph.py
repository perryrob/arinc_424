
from geo_json.geometry import distance_deg

class RouteGraph:

    def __init__(self, fix_routes={}, route_fixes={}):
        self.fix_routes = fix_routes
        self.route_fixes = route_fixes
        self.visited=[]
        self.possible_route=[]


    def distance(self, fix1, fix2):

        if fix2 is None: return 0
        
        return distance_deg( (fix1.longitude,fix1.latitude),
                             (fix2.longitude,fix2.latitude) )

        
    def get_fixes_from(self,name,route_fixes,BKWRD=False):
        ret_val = []
        accumulate = False

        if BKWRD:
            route_fixes.reverse()
            
        for fix in route_fixes:
            if fix.fix_id == name:
                accumulate=True
            if accumulate:
                ret_val.append(fix)

        return ret_val

    def traverse(self, from_fix, to_fix ):

        for route in self.fix_routes[from_fix.fix_id]:
            fwd_route_fixes = self.get_fixes_from(
                from_fix.fix_id,
                self.route_fixes[route.route_id]
            )
            bwd_route_fixes = self.get_fixes_from(
                from_fix.fix_id,
                self.route_fixes[route.route_id],
                True
            )
            for route_id in fwd_route_fixes + bwd_route_fixes:
                if route_id.route_id == 'V105':
                    print(route.route_id,fwd_route_fixes)
                    print(route.route_id,bwd_route_fixes)
                    xx
    def propose_route(self,DEP='',DES=''):

        possible_dep_routes = self.fix_routes[DEP]
        possible_des_routes = self.fix_routes[DES]

        return self.traverse( possible_dep_routes[0],
                              possible_des_routes[0] )
        
