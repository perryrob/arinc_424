
from geojson import Polygon, Point, LineString
from geojson import GeometryCollection, Feature


from .geometry import circle_center_polygon, line_center_angle


def VOR( radius=1, segments=36, center=(0,0), variation=0, properties={} ):

    geometry_collection = [
        Polygon(
            circle_center_polygon(radius, segments, center, variation ),
            properties={'line_color':'blue',
                        'line_width':5,
                        'fill_color':'blue',
                        'alpha':100,
                        'name':properties['name'],
                        'description':properties['frequency']
                        }
        ),
        Polygon(
            circle_center_polygon(0.25, 4, center, 0),
            properties={'line_color':'black',
                        'line_width':1,
                        'fill_color':'black',
                        'alpha':100,
                        'name':properties['name'],
                        'description':properties['frequency']
                        }
        ),
        LineString(
            line_center_angle( radius, center, variation),
            properties={'line_color':'blue',
                        'line_width':2,
                        }
        ),
        Point( center,
               properties={'name':properties['name'],
                           'description':properties['frequency'],
                           'FOO':'BAR'
                           }
              )
    ]
    gc = GeometryCollection( geometry_collection , properties=properties)
    return Feature(geometry=gc)

def NDB( radius=1, segments=36, center=(0,0), properties={} ):

    geometry_collection = [
        Polygon(
            circle_center_polygon(radius, segments, center),
            properties={'line_color':'aqua',
                        'line_width':0,
                        'fill_color':'aqua',
                        'alpha':100,
                        'name':properties['name'],
                        'description':properties['frequency']
                        }
        ),
        Polygon(
            circle_center_polygon(0.25, 4, center, 0),
            properties={'line_color':'black',
                        'line_width':1,
                        'fill_color':'black',
                        'alpha':100,
                        'name':properties['name'],
                        'description':properties['frequency']
                        }
        ),
         Point( center,
                properties={'name':properties['name'],
                            'description':properties['frequency']
                           }
              )
    ]
    gc = GeometryCollection( geometry_collection , properties=properties)
    return Feature(geometry=gc)

def WAYPOINT( radius=1, segments=36, center=(0,0), properties={} ):
    p = Polygon(
        circle_center_polygon(radius, segments, center),
        properties={'line_color':'black',
                    'line_width':1,
                    'fill_color':'red',
                    'alpha':200,
                    'name':properties['name'],
                    }
    )
    return Feature(geometry=p)

def AIRWAY( airways={}, route_id='', center=(0,0), properties={} ):

    if route_id is None: # None is passed in as a termination of the route
        geometry_collection=[]
        for route_id in airways.keys():
            for line_string in airways[route_id]:
                if type(line_string) == type(LineString()):
                    geometry_collection.append( line_string )
                
        gc = GeometryCollection( geometry_collection ,
                                 properties=properties)
        return Feature(geometry=gc)

    if route_id[0] in ['A','B','J', 'M', 'Q','R','Y']:
        return airways
    
    if route_id in airways.keys():
        # I ave at least 2 - n points on the route so I'm going to greate a
        # LineString with the last two points and replace the firt point with
        # the object
        airways[route_id].append([center,properties])
        
        desc_code = properties['description_code']

        p2_idx = len( airways[route_id] ) - 1
        p1_idx = p2_idx - 1
        
        p1_prop = airways[route_id][p1_idx][1]
        p2_prop = airways[route_id][p2_idx][1]
        
        airways[route_id][p1_idx] = LineString(
            [(airways[route_id][p1_idx][0],
              airways[route_id][p2_idx][0])],
            properties={'line_color':'black',
                        'line_width':2,
                        'fill_color':'black',
                        'alpha':255,
                        'name':route_id,
                        }
        )
    else:
        airways[route_id]=[[center,properties]]

    return airways

'''
    p2_idx = len( airways[route_id] )

    if p2_idx % 2 == 0:
        for i in range( p2_idx - 2, p2_idx): # last two positions in the list
            pp = airways[route_id][i] # Get the last 2 points
            center = pp[0]
            ss = pp[1]['SECTION_SUBSECTION']
            # Figure out if the center point passed in is associated with a
            # WAYPOINT, VOR or NDB
            if ss == 'D ':
                print('VOR')        
            elif ss == 'DB':
                print('NDB')
            elif ss == 'EA':
                print('WAYPOINT')
            else:
                print(ss,'UNK')
            print(i,center)
            pp[i] = center

'''        

