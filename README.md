# arinc_424

This python parser and database stuffer is designed to consume publicly
available file from the [Government FAA Website](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/)

## Requirements

To run this code you will need to install postgres for your appropriate operating system and make a connection available from where you run this python code. The default connection parameters in the code are:

'''Python
class DB_connect:

    def __init__(self, host='localhost',
                 database='arinc_424',
                 user='[USER]',
                 password='peer',
                 debug=False):
'''

## Installation of dependencies on Ubuntu

'''Bash

$ sudo apt install postgresql postgresql-contrib libpq-dev
$ mkdir [target_dir]
$ python3 -m venv env
$ source ./env/bin/activate
$ pip install psycopg2

'''
## Setting up postgres

Follow google instructions for setting up a "arinc_424" database for your user account on localhost.



