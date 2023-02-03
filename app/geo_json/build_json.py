
from geojson import Polygon, Point, LineString,MultiLineString
from geojson import GeometryCollection, Feature


from .geometry import circle_center_polygon, line_center_angle, true_course_deg
from .geometry import rad_to_deg, point_project

VOR_RADIUS=2.5
NDB_RADIUS=1.0
WAYPOINT_RADIUS=0.25

ICON_PATH='http://maps.google.com/mapfiles/kml/'

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
                           'icon':ICON_PATH+'shapes/polygon.png'
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
                            'description':properties['frequency'],
                            'icon':ICON_PATH+'shapes/donut.png'
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

def AIRWAY( airways={}, waypoint_types={}, route_id='',
            center=(0,0), properties={} ):

    if route_id is None:
        geometry_collection=[]
        for route_id in airways.keys():
            points = airways[route_id]
            section_subsections = waypoint_types[route_id]
                
            for i in range(1,len(points)):
                p1 = i-1
                p2 = i
                pp = [points[p1],points[p2]]
                pp_crs = [true_course_deg(pp[0],pp[1],True), # OBD crs
                          true_course_deg(pp[1],pp[0],True)] # IBD crs
                props = waypoint_types[route_id][p1:p2+1]

                # Outboud properties
                description='MEA: ' + \
                    str(props[0].get('min_altitude','UNK')) + ' ' +\
                    'Outbound Crs: ' + str(props[0].get('outbound_course','UNK'))
                
                modified_pp =[]
                for ii  in range(0,2):
                    section_subsection = props[ii]['SECTION_SUBSECTION']
                    p   = pp[ii]
                    crs = pp_crs[ii]
                    f_point = None
                    if section_subsection == 'D ':
                        modified_pp.append(point_project( p,
                                                          crs,
                                                          VOR_RADIUS ))
                        geometry_collection.append(
                            Point(
                                modified_pp[-1:][0],
                                properties={
                                    'name':route_id,
                                    'description': description,
                                    'icon':ICON_PATH+'paddle/wht-diamond.png'
                                }
                            )
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
                                        'desription':description
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
        airways[route_id].append(center)
        waypoint_types[route_id].append(properties)
    else:
        airways[route_id]=[center]
        waypoint_types[route_id] = [properties]
    return airways

def RUNWAY(runways={},airport_id='',rwy=[], feature_values={}):

    if airport_id is None:
        geometry_collection=[]
        for airport_id in runways.keys():
            runway = runways[airport_id]
            ap_icon=ICON_PATH+'paddle/grn-stars.png'
            if runway['airport']['ifr'] =='Y':
                ap_icon=ICON_PATH+'paddle/blu-stars.png'
            
            geometry_collection.append(
                Point( runway['center'],
                       properties={
                           'name':airport_id,
                           'description':airport_id,
                           'icon':ap_icon
                       }
                      )
            )
        gc = GeometryCollection( geometry_collection ,
                                 properties={})
        return Feature(geometry=gc)
    
    else:
        if airport_id in runways.keys():
            runways[airport_id]['runways'].append(
                {
                    'id':rwy[feature_values['r_id']],
                    'length':rwy[feature_values['r_length']],
                    'magnetic_bearing':rwy[feature_values['r_magnetic_bearing']],
                    'latitude':rwy[feature_values['r_latitude']],
                    'longitude':rwy[feature_values['r_longitude']],
                    'gradiant':rwy[feature_values['r_gradiant']],
                    'elevation':rwy[feature_values['r_elevation']],
                    'displaced_distance':rwy[feature_values['r_displaced_distance']],
                    'width':rwy[feature_values['r_width']],
                    'description':rwy[feature_values['r_description']]
                }
            )
        else:
            # New airport
            runways[airport_id]={
                'center': (rwy[feature_values['a_longitude']],
                           rwy[feature_values['a_latitude']]),
                'airport':{
                    'ifr':rwy[feature_values['a_ifr']],
                    'mag_variation':rwy[feature_values['a_mag_variation']],
                    'elevation':rwy[feature_values['a_elevation']],
                },
                'runways':[]
            }
    return runways
