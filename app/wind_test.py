
from wind.get_wind import Wind
from db.DB_Manager import DB_connect

if __name__ == '__main__':

    try:
        db_connect = DB_connect()
        conn = db_connect.get_connection()
        w = Wind(conn=conn)
        
        for a in range(0,39000,500):
            print('TUS',w.get_airdata('TUS',a))

    except Exception as e:
        print('Unable to connect to the database...')
        raise(e)


