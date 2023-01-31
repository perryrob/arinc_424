
from geojson import Polygon, Point, LineString,MultiLineString
from geojson import GeometryCollection, Feature


from .geometry import circle_center_polygon, line_center_angle, true_course_deg
from .geometry import rad_to_deg, point_project

VOR_RADIUS=2.5
NDB_RADIUS=1.0
WAYPOINT_RADIUS=0.25

def VOR( radius=1, segments=36, center=(0,0), variation=0, properties={} ):

    name = properties['name']
    
    geometry_collection = [
        Polygon(
            circle_center_polygon(radius, segments, center, variation ),
            properties={'line_color':'blue',
                        'line_width':5,
                        'fill_color':'blue',
                        'alpha':100,
                        'name':name,
                        'description':properties['frequency']
                        }
        ),
        Polygon(
            circle_center_polygon(0.25, 4, center, 0),
            properties={'line_color':'black',
                        'line_width':1,
                        'fill_color':'black',
                        'alpha':100,
                        'name':name,
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

def AIRWAY_NEW( airways={}, route_id='', center=(0,0), properties={} ):

    if route_id is None: # None is passed in as a termination of the route
        geometry_collection=[]
        for route_id in airways.keys():
            points = None
            airway_lines = []
            for point_props in airways[route_id]:
                raw_point = [p[0] for p in airways[route_id]]
                props =     [p[1] for p in airways[route_id]]
                for i in range(1,len(raw_point)):
                    try:
                        p1 = raw_point[i-1]
                        p2 = raw_point[i]

                        crs_p1 = true_course_deg(p1,p2)
                        crs_p2 = true_course_deg(p2,p1)
                        
                        prop_1 = props[i-1]
                        prop_2 = props[i]

                        pcp = [[p1,crs_p1,prop_1],[p2,crs_p2,prop_2]]

                        new_point = []
                    except Exception as e:
                        print(route_id)
                        raise(e)

                # airway_lines.append((new_point[0],new_point[1]))
                airway_lines.append((p1,p2))
                    
                geometry_collection.append(MultiLineString(
                    airway_lines,
                    properties={'line_color':'black',
                                'line_width':2,
                                'fill_color':'black',
                                'alpha':255,
                                'name':route_id,
                                }
                ))                    
        # All routes
        gc =  GeometryCollection( geometry_collection )
        return Feature(geometry=gc)

    if route_id in airways.keys():
        airways[route_id].append([center,properties])
    else:
        airways[route_id]=[[center,properties]]

    return airways

def AIRWAY( airways={}, waypoint_types={}, route_id='',
            center=(0,0), properties={} ):

    if route_id is None:
        geometry_collection=[]
        for route_id in airways.keys():
            points = airways[route_id]
            section_subsections = waypoint_types[route_id]
                
            for i in range(1,len(points)):

                pp = [points[i-1],points[i]]
                pp_crs = [true_course_deg(pp[0],pp[1],True),
                          true_course_deg(pp[1],pp[0],True)]
                types = waypoint_types[route_id][i-1:i+1]

                modified_pp =[]
                for ii  in range(0,2):
                    section_subsection = types[ii]
                    p   = pp[ii]
                    crs = pp_crs[ii]
                    f_point = None
                    if section_subsection == 'D ':
                        modified_pp.append(point_project( p,
                                                          crs,
                                                          VOR_RADIUS ))
                        f_point = Point(
                            modified_pp[-1:],
                            properties={'name':route_id}
                        )

                    elif section_subsection == 'DB':
                        modified_pp.append(point_project( p,
                                                          crs,
                                                          NDB_RADIUS))
                    elif section_subsection == 'EA':
                        modified_pp.append(point_project( p,
                                                          crs,
                                                          WAYPOINT_RADIUS))
                try:
                    geometry_collection.append(
                        LineString(
                            modified_pp,
                            properties={'line_color':'black',
                                        'line_width':2,
                                        'fill_color':'black',
                                        'alpha':255,
                                        'name':route_id,
                                        }
                        )
                    )
                    
                    # if f_point is not None:
                     #   geometry_collection.append(f_point)
                      #   f_point = None
                    
                except Exception as e:
                    print( e )
                    print('err',route_id, airways[route_id])
                    
        gc = GeometryCollection( geometry_collection ,
                                 properties=properties)
        return Feature(geometry=gc)
    
    if route_id in airways.keys():
        airways[route_id].append(center)
        waypoint_types[route_id].append(properties['SECTION_SUBSECTION'])
    else:
        airways[route_id]=[center]
        waypoint_types[route_id] = [properties['SECTION_SUBSECTION']]
    return airways
