# arinc_424

## Disclaimer

Do not use this as a primary source of navigation. It is for instructional and planning purposes only. Always verify with official sources.

This python parser and database stuffer is designed to consume publicly
available data files from the [Government FAA Website](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/)

## Useage

There are currently 2 programs in app. arinc_424_18_parser.py and test.py. The first parses the CIFP data and the second one, test.py creates a geojson and kml file that display NDBs, VORs, waypoints and airways.

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

* Change to the app directory and run
```
python arinc_parse.py
```


## Notes

You don't have to use the database simply comment out

``` Python
db_connect = DB_connect()


for statement in drop_statements:
    try:
        db_connect.exec( statement )        
    except Exception as e:
        pass

for statement in create_statements:
    db_connect.exec( statement,False )


arinc_data = DB_ARINC_data( supported, ARINC_424_PARSE_DEF, parsed_record_dict )
insert_arinc_data_list = arinc_data.create_inserts()

for insert in insert_arinc_data_list:
    db_connect.exec( insert, False )

db_connect.commit()
db_connect.close()
```

## TODO

* Handle continuations
* Add more formatters