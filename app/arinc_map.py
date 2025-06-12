
from build_geojson_kml import VOR_geom, NDB_geom, WAYPOINT_geom
from build_geojson_kml import AIRWAY_geom, AIRPORT_geom, fly_center
from build_geojson_kml import PROPOSED_ROUTE_geom, fly_edges
from build_geojson_kml import ROUTE_geom
from build_geojson_kml import MERGE_RNAV_VOR

from weather.metars import Metars
from weather.tafs import Tafs
from weather.airsigmets import AirSigmets
from weather.aircraftreport import AircraftReport


from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from db.post_create_sql import POST_CREATE_SQL

from translator.Translators import FIELD_REFERENCES
from spec.arinc_424_23_parser import ARINC_424_PARSE_DEF

from CONFIG import ARINC424_INPUT_FILE,ARINC_DATA_FILE

from parser.arinc_parse import  cleanup_db,setup_db,parse,load_db,post_create_db

from translator import Translators
from translator.Translators import FIELD_REFERENCES

from route.find_route import distance_crs,closest_wpts, Route

from weather.wind import Wind

import argparse

SUPPORTED_SECTIONS_SUBSECTIONS=[
    ('A','S'), # MORA
    ('D',' '), # VOR
    ('D','B'), # NDB
    ('E','A'), # Waypoints
    ('E','R'), # Airways
    ('H','A'), # Helipads
    ('H','C'), # Terminal Waypoints
    ('H','F'), # Approaches
    ('H','S'), # MSA
    ('P','A'), # Airports
    ('P','G'), # Runways
    ('P','I'), # Localizer
    ('P','N'), # airport Navaid
    ('P','P'), # airport waypoint
    ('P','D'), # SID
    ('P','E'), # STAR
    ('P','F'), # Approaches
    ('P','S'), # MSA
    ('U','C'), # CLASS B,C and D Airsapce
    ('U','R'), # Special Use Airspace    
]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Write KMZ or json files generated from a parsed CIFP file.'
    )

    parser.add_argument('-c','--cifp',help='Input CIFP file.',
                        default='app/cifp/FAACIFP18')
    
    for val in ['vor','ndb','waypoint','airway','airport', 'all_pts']:
        parser.add_argument('--'+val, help='create '+val+' KMZ and/or json file',
                        action='store_true')

    parser.add_argument('--debug', help='set debug',
                        action='store_true')

    parser.add_argument('--clean_db',help='Purge all data and tabless. '+\
                        'then recreate db with blank schema.',action='store_true'
                        )

    parser.add_argument('--recreate_db',help='Purge all data and tabless. '+\
                        'then recreate db with blank schema.'+\
                        'parse CIFP file and load new data.',action='store_true'
                        )

    parser.add_argument('--route_format',help='Output the data in route format. '+\
                        'Can be fed into --route',
                        action='store_true'
                        )

    parser.add_argument('--fly_route',help='load the route into the'+\
                        '--route_file',
                        action='store_true'
                        )
    
    parser.add_argument('--format_430',help='Output the data in easy to enter '+\
                        '430 format',
                        action='store_true'
                        )

    parser.add_argument('--fuel_range',help='Enter fuel stop range in NM or hours. '+\
                        'The code will assume anything over 40 hours is actual range '+\
                        'and anything less is time in hours.',
                        type=int,
                        default=5
                        )
    parser.add_argument('--wind_fcast',help='Enter the wind forcast time 6,12,24 ',
                        type=int,
                        default=None
                        )
    
    parser.add_argument('--fly_to', nargs=3, action='append', type=float,
                        metavar=('lon', 'lat', 'alt'),
                        help='Enter lon(deg) lat(deg) alt(m) for VIEW.kmz',
                        default=None
                        )

    parser.add_argument('--max_alt', type=int,
                        help='Enter maximum desired altitude for routing',
                        default=18000
                        )
    parser.add_argument('-a','--alt', type=int,
                        help='Enter altitude altitude for wind'
                        )

    parser.add_argument('-s','--speed', type=int,
                        help='Enter true airspeed.',
                        default=165
                        )

    
    parser.add_argument('--airway_types', nargs='+', type=str,
                        help='Enter airway type: V,T,J',
                        default=['V','T','J']
                        )

    parser.add_argument('--waypoint_types', nargs='+', action='append', type=str,
                        help='Enter airway type: W  ,C ,R ,W',
                        default=['W  ','C  ','R  ','W  ']
                        )
    
    parser.add_argument('--route', nargs='+', action='append', type=str,
                        help='Enter a route airports waypoints vors',
                        default=None
                        )
    parser.add_argument('--proposed_route', nargs=2, action='append', type=str,
                        help='Enter a route airports waypoints vors',
                        default=None
                        )
    parser.add_argument('--route_file', type=str,
                        help='Optional file BASE name of the route KMZ/JSON file. Levae off'+\
                        ' the .kmz or .json suffix',
                        default='ROUTE'
                        )
    

    parser.add_argument('--weather_stations',help='Load Weather reporint locations '+\
                        'into the database.',action='store_true'
                        )

    
    args=parser.parse_args()

    conn = None
    db_connect = None
    try:
        db_connect = DB_connect()
        conn = db_connect.get_connection()
    except Exception as e:
        print('Unable to connect to the database...')
        raise(e)

    db_tables = DB_ARINC_Tables( SUPPORTED_SECTIONS_SUBSECTIONS,
                                 ARINC_424_PARSE_DEF,
                                 FIELD_REFERENCES)
    if args.clean_db:
        cleanup_db(db_connect,db_tables)
        setup_db(db_connect,db_tables)

    if args.recreate_db:
        cleanup_db(db_connect,db_tables)        
        setup_db(db_connect,db_tables)
        parsed_record_dict = parse(args.cifp,
                                   SUPPORTED_SECTIONS_SUBSECTIONS,
                                   {}, Translators)
    
    
        load_db( db_connect, ARINC_424_PARSE_DEF,
                 SUPPORTED_SECTIONS_SUBSECTIONS, parsed_record_dict)

        post_create_db( db_connect )
        MERGE_RNAV_VOR(conn)
        conn.commit()
    
    if args.vor:
        VOR_geom(conn)

    if args.ndb:
        NDB_geom(conn)

    if args.waypoint:
        WAYPOINT_geom(conn,waypoint_types=args.waypoint_types)
        
    if args.airway:
        AIRWAY_geom(conn,airway_types=args.airway_types)
        
    if args.airport:
        AIRPORT_geom(conn)

    if args.all_pts:
        VOR_geom(conn)
        NDB_geom(conn)
        WAYPOINT_geom(conn,waypoint_types=args.waypoint_types)
        AIRWAY_geom(conn,airway_types=args.airway_types)
        AIRPORT_geom(conn)        

    if args.weather_stations:
        s = Stations(conn)
        #Metars(conn)
        #Tafs(conn)
        #AirSigmets(conn)
        #AircraftReport(conn)

    if  args.fly_to is not None:
        fly_center(args.fly_to[0])


    if args.route is not None:

        fuel_stops =[]
        edges,fixes = distance_crs( conn, args.route )

        wind = Wind( conn=conn , time=args.wind_fcast)

        route = Route( conn, edges[0],edges[len(edges)-1],
                       fuel_duration = args.fuel_range,
                       max_alt = args.max_alt,
                       AIRWAY_TYPES=args.airway_types,
                       cruise_alt = args.alt,
                       cruise_speed = args.speed,
                       wind=wind,
                       edges=edges)
        
        if args.format_430:
            route.format_430()

        if args.speed and args.alt:
            edges,total_distance,fuel_stops = route.get_wind_route()
            
        PROPOSED_ROUTE_geom( edges, fuel_stops, file_name=args.route_file )

        if args.fly_route:
            fly_edges(edges, roll=0, tilt=0,filename='VIEW.kmz')

        else:        
            if args.route_format:
                for i in range(0,len(edges)):
                    edge = edges[i]
                    if i == 0:
                        print(edge.fix1,end=' ')
                    print(edge.fix2,end=' ')
                print('')
            else:
                print(route)
    
    if args.proposed_route is not None:

        fuel_stops =[]
        
        dep_edge,des_edge = closest_wpts( conn, args.proposed_route[0][0],
                                        args.proposed_route[0][1],
                                        args.airway_types)
        wind = None
        edges = None
        total_distance = None

        if args.wind_fcast not in [6,12,24,None]:
            raise Exception( 'Warning wind forcast must be 6,12,24 hours not '+str(args.wind_fcast))

        wind = None
        if args.wind_fcast:
            wind = Wind( conn=conn , time=args.wind_fcast)

        route = Route( conn, dep_edge,des_edge,
                       fuel_duration = args.fuel_range,
                       max_alt = args.max_alt,
                       AIRWAY_TYPES=args.airway_types,
                       cruise_alt = args.alt,
                       cruise_speed = args.speed,
                       wind=wind )

        if args.debug:
            PROPOSED_ROUTE_geom( wind. get_delaunay_edges(), file_name='station_delauney',color_override='aqua')
        
        if args.format_430:
            route.format_430()
            
        if args.speed and args.alt:
            edges,total_distance,fuel_stops = route.get_wind_route()
                    
        PROPOSED_ROUTE_geom( edges, fuel_stops, file_name=args.route_file )

        if args.fly_route:
            fly_edges(edges, roll=0, tilt=0,filename='VIEW.kmz')

        else:        
            if args.route_format:
                for i in range(0,len(edges)):
                    edge = edges[i]
                    if i == 0:
                        print(edge.fix1,end=' ')
                    print(edge.fix2,end=' ')
                print('')
            else:
                print(route)
    
    conn.commit()
    conn.close()
    
