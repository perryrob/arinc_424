from weather.json_to_sql import JSON_SQL
from weather.csv_to_json import Csv_to_JSON

class Tafs:
        def __init__(self, conn, input_file='app/aviation_weather/tafs.cache.csv'):

            ctj = Csv_to_JSON( input_file )    
            jsql=JSON_SQL('taf',ctj.get_json())
            
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

