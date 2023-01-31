
from geojson import Polygon, Point, LineString,MultiLineString
from geojson import GeometryCollection, Feature


from .geometry import circle_center_polygon, line_center_angle, true_course_deg
from .geometry import rad_to_deg, point_project

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
    if name == 'TUS':
        print('Polygon',
              circle_center_polygon(radius, segments, center, variation ))
        print('Line',
              line_center_angle( radius, center, variation))

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
            if route_id != 'V393': ######### force testing
                continue
            points = None
            airway_lines = []
            for point_props in airways[route_id]:
                raw_points = [p[0] for p in airways[route_id]]
                props =  [p[1] for p in airways[route_id]]

                for i in range(1,len(raw_points)):
                    try:
                        p1 = raw_points[i-1]
                        p2 = raw_points[i]

                        crs_p1 = true_course_deg(p1,p2)
                        crs_p2 = true_course_deg(p2,p1)
                        
                        prop_1 = props[i-1]
                        prop_2 = props[i]

                        pcp = [[p1,crs_p1,prop_1],[p2,crs_p2,prop_2]]

                        new_point = []
                        for p,crs,prop in pcp:
                            # (D ), (DB), (EA)
                            if prop['SECTION_SUBSECTION'] == 'D ':
                                new_point.append(
                                    point_project( p,
                                                   crs,
                                                   prop['VOR_RADIUS']))
                            elif prop['SECTION_SUBSECTION'] == 'DB':
                                new_point.append(
                                    point_project( p,
                                                   crs,
                                                   prop['NDB_RADIUS']))
                            elif prop['SECTION_SUBSECTION'] == 'EA':
                                new_point.append(
                                    point_project( p,
                                                   crs,
                                                   prop['WAYPOINT_RADIUS']))
                            print( crs, p , new_point )
                    except Exception as e:
                        print(route_id)
                        raise(e)
                airway_lines.append((new_point[0],new_point[1]))
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
