from weather.json_to_sql import JSON_SQL
from weather.csv_to_json import Csv_to_JSON

from metar_taf_parser.parser.parser import MetarParser

class Metars:
        def __init__(self, conn, input_file='app/aviation_weather/metars.cache.csv'):

            ctj = Csv_to_JSON( input_file )    
            err_count = 0

            for metar in ctj.get_json():
                try:
                    m = MetarParser().parse( metar['raw_text'])
                except ValueError as ve:
                    err_count = err_count + 1
                    print(err_count,str(ve),metar['raw_text'])
                except:
                    pass
                    
            jsql=JSON_SQL('metar',ctj.get_json())

            try:
                cursor = conn.cursor()
                cursor.execute( jsql.table_drop_sql() )
                cursor.close()
                conn.commit()
            except:
                conn.rollback()
        
            cursor = conn.cursor()
            cursor.execute( jsql.table_create_sql() )
            cursor.close()
            conn.commit()
            
            cursor = conn.cursor()
            for insert in jsql.create_inserts():
                cursor.execute( insert )

            cursor.close()
            conn.commit()
