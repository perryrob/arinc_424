
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
        )
    ]
    gc = GeometryCollection( geometry_collection , properties=properties)
    return Feature(geometry=gc)

def WAYPOINT( radius=1, segments=36, center=(0,0), properties={} ):
    p = Polygon(
        circle_center_polygon(radius, segments, center),
        properties={'line_color':'black',
                    'line_width':1,
                    'fill_color':'black',
                    'alpha':200,
                    'name':properties['name'],
                    }
    )
    return Feature(geometry=p)

def AIRWAY( airways={}, route_id='', center=(0,0), properties={} ):

    if route_id is None:
        geometry_collection=[]
        for route_id in airways.keys():
            if route_id[0] in ['A','B','J', 'M', 'Q','R','Y']:
                continue # ignore
            try:                
                geometry_collection.append(
                    LineString(
                        airways[route_id],
                        properties={'line_color':'black',
                                    'line_width':2,
                                    'fill_color':'black',
                                    'alpha':255,
                                    'name':route_id,
                                    }
                    )
                )
            except Exception as e:
                print( e )
                print('err',route_id, airways[route_id])
                
        gc = GeometryCollection( geometry_collection ,
                                 properties=properties)
        return Feature(geometry=gc)
    
    if route_id in airways.keys():
        points = airways[route_id].append(center)
    else:
        airways[route_id]=[center]

    return airways
