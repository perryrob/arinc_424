
from weather.json_to_sql import JSON_SQL


class Stations:
    def __init__(self, conn, input_file='app/aviation_weather/stations.cache.json'):
        with open( input_file, 'r') as f:
            txt = f.read()
            
        jsql=JSON_SQL('station',txt)
        # print(jsql.table_drop_sql())
        # print(jsql.table_create_sql())
        # print(jsql.create_inserts())
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
            
