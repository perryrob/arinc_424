# Arinc 424 Parser to GEOJson and KML

## Disclaimer

Do not use this as a primary source of navigation. It is for instructional and planning purposes only. Always verify with official sources.

This python parser and database stuffer is designed to consume publicly
available data files from the [Government FAA Website](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/)

## Useage

There is one program in app. arinc_map.py. It can take several arguments to produce KMZ files that are loaded into Google Earth pro.

![TUS_Image](img/TUS_nav.png?raw=true)

## Requirements

To run this code you will need to install postgres for your appropriate operating system and make a connection available from where you run this python code. The default connection parameters in the code are:

``` Python

class DB_connect:

    def __init__(self, host='localhost',
                 database='arinc_424',
                 user='[USER]',
                 password='peer',
                 debug=False):
```

## Installation of dependencies on Ubuntu

```

$ sudo apt install postgresql postgresql-contrib libpq-dev
$ mkdir [target_dir]
$ python3 -m venv env
$ source ./env/bin/activate
$ pip install -r requirements.txt

```
## Setting up postgres

Follow google instructions for setting up a "arinc_424" database for your user account on localhost.

## Running

* First get the latest CIFP file. Edit update_cifp after visiting the [Government FAA Website](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/)

* then run:

```
update_cifp.sh
```

* Run
```
python app/arinc_map.py -h

```
```
usage: arinc_map.py [-h] [-c CIFP] [--vor] [--ndb] [--waypoint] [--airway] [--airport] [--all_pts]
                    [--clean_db] [--recreate_db] [--route_format] [--fly_route] [--format_430]
                    [--fly_to lon lat alt] [--airway_types AIRWAY_TYPES [AIRWAY_TYPES ...]]
                    [--waypoint_types WAYPOINT_TYPES [WAYPOINT_TYPES ...]] [--route ROUTE [ROUTE ...]]
                    [--proposed_route PROPOSED_ROUTE PROPOSED_ROUTE] [--route_file ROUTE_FILE]

Write KMZ or json files generated from a parsed CIFP file.

optional arguments:
  -h, --help            show this help message and exit
  -c CIFP, --cifp CIFP  Input CIFP file.
  --vor                 create vor KMZ and/or json file
  --ndb                 create ndb KMZ and/or json file
  --waypoint            create waypoint KMZ and/or json file
  --airway              create airway KMZ and/or json file
  --airport             create airport KMZ and/or json file
  --all_pts             create all_pts KMZ and/or json file
  --clean_db            Purge all data and tabless. then recreate db with blank schema.
  --recreate_db         Purge all data and tabless. then recreate db with blank schema.parse CIFP file and
                        load new data.
  --route_format        Output the data in route format. Can be fed into --route
  --fly_route           load the route into the--route_file
  --format_430          Output the data in easy to enter 430 format
  --fly_to lon lat alt  Enter lon(deg) lat(deg) alt(m) for VIEW.kmz
  --airway_types AIRWAY_TYPES [AIRWAY_TYPES ...]
                        Enter airway type: V,T,J
  --waypoint_types WAYPOINT_TYPES [WAYPOINT_TYPES ...]
                        Enter airway type: W ,C ,R ,W
  --route ROUTE [ROUTE ...]
                        Enter a route airports waypoints vors
  --proposed_route PROPOSED_ROUTE PROPOSED_ROUTE
                        Enter a route airports waypoints vors
  --route_file ROUTE_FILE
                        Optional file BASE name of the route KMZ/JSON file. Levae off the .kmz or .json
                        suffix
```


## DB Tables Created

```
 Schema |        Name         
--------+---------------------
 public | airport             
 public | airport_msa         
 public | airport_ndb         
 public | airport_waypoint    
 public | airway              
 public | approach            
 public | controlled_airspace 
 public | heliport            
 public | heliport_approach   
 public | heliport_msa        
 public | heliport_waypoint   
 public | localizer           
 public | mora                
 public | ndb                 
 public | runway              
 public | sid                 
 public | special_airspace    
 public | star                
 public | vor                 
 public | waypoint            
```

## Examples of operation

### Create a direct route from Tucson (KTUS) to Benson AZ (E95)

The following command line will create a direct route from KTUS to E95 and create a file DIRECT.kmz
```
$ python app/arinc_map.py --route  KTUS E95 --route_file DIRECT
DIRECT.kmz
FIX	CRS(t)	   DIS(nm)
===========================
KTUS 	 E95 	 30.46198543543584
---------------------------
total:   	 30.5
```
The next command line will create a direct route from KTUS TRICO E95 and create a file TRICO.kmz
```
$ python app/arinc_map.py --route  KTUS TRICO E95 --route_file TRICO 
TRICO.kmz
FIX	CRS(t)	   DIS(nm)
===========================
KTUS 	 TRICO 	 17.593860683342044
TRICO 	 E95 	 13.118881455810186
---------------------------
total:   	 30.7
```
Finally the last example command will create a proposed route using a Dijkstra least distance algorithm that uses airways and fixes to create the route. At short distances like a 30 mile trip between Tucson and Benson, its not ideal.
```
$ python app/arinc_map.py --airway_types V T --proposed_route  KTUS E95 --route_file PROPOSED
PROPOSED.kmz
KTUS
	direct-|1.8|
TUS
	T310-|20.0|
SULLI
	T310-V66-|5.0|
MESCA
	direct-|9.1|
E95
-----------------------------
Total Distance: 35.851068083265446
```
### All 3 routes are shown below

![TUS_Routes](img/routes.png?raw=true)

## Notes

I've tested the KML file on Google Earth Pro and it works correctly.

```

## TODO
* respect MEAs
* Add wind to cost calculation
* Webify
* Handle continuations
* Add more formatters
