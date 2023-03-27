
from build_geojson_kml import VOR_geom, NDB_geom, WAYPOINT_geom
from build_geojson_kml import AIRWAY_geom, AIRPORT_geom, fly_center
from build_geojson_kml import PROPOSED_ROUTE_geom, fly_edges
from build_geojson_kml import ROUTE_geom

from db.DB_Manager import  DB_ARINC_Tables, DB_connect, DB_ARINC_data
from db.post_create_sql import POST_CREATE_SQL

from translator.Translators import FIELD_REFERENCES
from spec.arinc_424_18_parser import ARINC_424_PARSE_DEF

from CONFIG import ARINC424_INPUT_FILE,ARINC_DATA_FILE

from arinc_parse import  cleanup_db,setup_db,parse,load_db,post_create_db
from arinc_parse import  post_create_db_scripts

from translator import Translators
from translator.Translators import FIELD_REFERENCES

from route.find_route import distance_crs,closest_wpts,find_route

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
    
    for val in ['vor','ndb','waypoint','airway','airport']:
        parser.add_argument('--'+val, help='create '+val+' KMZ and/or json file',
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

    parser.add_argument('--fly_to', nargs=3, action='append', type=float,
                        metavar=('lon', 'lat', 'alt'),
                        help='Enter lon(deg) lat(deg) alt(m) for VIEW.kmz',
                        default=None
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
        post_create_db_scripts( db_connect )
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

    if  args.fly_to is not None:
        fly_center(args.fly_to[0])


    if args.route is not None:

        edges,fixes = distance_crs( conn, args.route )

        ROUTE_geom( fixes,file_name=args.route_file )

        if args.format_430:
            next_edge = None
            total_distance = 0.0
            fix_dis = 0
            for i in range(1,len(edges)):                
                edge = edges[i-1]
                next_edge = edges[i]

                if i-1 == 0:
                    print(edge.fix1)
                total_distance = total_distance + edge.distance
                fix_dis = fix_dis + edge.distance
                if not edge.is_colinear(next_edge):
                    print('\t'+edge.name+'|'+'{:3.1f}'.format(fix_dis)+'|')
                    print(next_edge.fix1)
                    fix_dis = 0
                    
            print('\t'+next_edge.name+'|'+\
                  '{:3.1f}'.format(next_edge.distance)+'|')
            print(next_edge.fix2)
            total_distance = total_distance + next_edge.distance
            print('-----------------------------')
            print('Total Distance:', '{:4.1f}'.format(total_distance))
        else:
            print('FIX\tCRS(t)\t   DIS(nm)')
            print('===========================')
            dis=0
            for f in fixes[1:]: # Gotta figure out why the 0th one dups
                dis = dis + f.get_edges()[0].get_distance()
                print(f.get_edges()[0].fix1,'\t',
                      f.get_edges()[0].fix2,'\t',
                      '{:3.1f}'.format(f.get_edges()[0].get_distance()))
                
            print('---------------------------')
            print('total:   \t','{:4.1f}'.format(dis))

        
        
    if args.proposed_route is not None:
        
        dep_edge,des_edge = closest_wpts( conn, args.proposed_route[0][0],
                                        args.proposed_route[0][1],
                                        args.airway_types)

        edges,total_distance = find_route(conn,
                                          dep_edge,
                                          des_edge,
                                          args.airway_types)

        PROPOSED_ROUTE_geom( edges, file_name=args.route_file )

        if args.fly_route:
            fly_edges(edges, roll=0, tilt=0,filename='VIEW.kmz')

        if args.format_430:            
            next_edge = None
            total_distance = 0.0
            fix_dis = 0
            non_colinear_edges = []
            for i in range(1,len(edges)):                
                edge = edges[i-1]
                next_edge = edges[i]

                if i-1 == 0:
                    print(edge.fix1)
                    non_colinear_edges.append(edge)

                total_distance = total_distance + edge.distance
                fix_dis = fix_dis + edge.distance

                if not edge.is_colinear(next_edge):
                    print('\t'+edge.name+'|'+'{:3.1f}'.format(fix_dis)+'|')
                    print(next_edge.fix1)
                    fix_dis = 0
                    non_colinear_edges.append(next_edge)
                    
            print('\t'+next_edge.name+'|'+\
                  '{:3.1f}'.format(next_edge.distance)+'|')
            print(next_edge.fix2)

            non_colinear_edges.append(next_edge)
            total_distance = total_distance + next_edge.distance

            print('-----------------------------')
            print('Total Distance:', '{:4.1f}'.format(total_distance))
            if args.fly_route:
                fly_edges(non_colinear_edges, roll=0, tilt=0,filename='VIEW.kmz')
        else:        
            if args.route_format:
                for i in range(0,len(edges)):
                    edge = edges[i]
                    if i == 0:
                        print(edge.fix1,end=' ')
                    print(edge.fix2,end=' ')
                print('')
            else:
                non_colinear_edges = []
                for i in range(0,len(edges)):
                    edge = edges[i]
                    if i == 0:
                        print(edge.fix1)
                    print('\t'+edge.name+'|'+'{:3.1f}'.format(edge.distance)+'|')
                    print(edge.fix2)
                    non_colinear_edges.append(edge)
                print('-----------------------------')
                print('Total Distance:', '{:4.1f}'.format(total_distance))
                if args.fly_route:
                    fly_edges(non_colinear_edges, roll=0, tilt=0,filename='VIEW.kmz')
            
    conn.commit()
    conn.close()
