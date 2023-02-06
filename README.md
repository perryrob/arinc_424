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
python app/arinc_map.py -h

```
```
usage: arinc_map.py [-h] [-c CIFP] [--vor] [--ndb] [--waypoint] [--airway] [--airport] [--clean_db] [--recreate_db] [--fly_to lon lat alt]

Write KMZ or json files generated from a parsed CIFP file.

optional arguments:
  -h, --help            show this help message and exit
  -c CIFP, --cifp CIFP  Input CIFP file.
  --vor                 create vor KMZ and/or json file
  --ndb                 create ndb KMZ and/or json file
  --waypoint            create waypoint KMZ and/or json file
  --airway              create airway KMZ and/or json file
  --airport             create airport KMZ and/or json file
  --clean_db            Purge all data and tabless. then recreate db with blank schema.
  --recreate_db         Purge all data and tabless. then recreate db with blank schema.parse CIFP file and load new data.
  --fly_to lon lat alt  Enter lon(deg) lat(deg) alt(m) for VIEW.kmz
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