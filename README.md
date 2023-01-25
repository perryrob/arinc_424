# Arinc 424 Parser to GEOJson and KML

## Disclaimer

Do not use this as a primary source of navigation. It is for instructional and planning purposes only. Always verify with official sources.

This python parser and database stuffer is designed to consume publicly
available data files from the [Government FAA Website](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/)

## Useage

There are currently 2 programs in app. arinc_424_18_parser.py and build_geojson_kml.py. The first parses the CIFP data and the second one, build_geojson_kml.py creates a geojson and kml file that display NDBs, VORs, waypoints and airways. The files created are ARINC_DATA_FILE.[geojson,kml]

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
$ pip install psycopg2

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
python app/arinc_parse.py
python app/build_geojson_kml.py

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


## Notes

I've tested the KML file on Google Earth Pro and it works correctly.

```

## TODO

* Handle continuations
* Add more formatters