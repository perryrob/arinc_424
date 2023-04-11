
from math import fabs
from datetime import date
TABLE_NAME=0
SELECT=1
COLUMNS=2
ETL_SCRIPT=3


def create_insert( a_list ):
    ret_val = ''
    for i in a_list:
        if type(i) == str:
            ret_val = ret_val + "'{item}',".format(item=i)
        elif i == None:
            ret_val = ret_val + 'NULL,'
        elif type(i)  == date:
            ret_val = ret_val + "'{DATE}',".format(DATE=i.strftime('%Y-%m-%d'))
        else:
            ret_val = ret_val + str(i) + ','
    return ret_val[:-1]


def resolve_none_defaults( conn, sql_tupple ):
    column_sql = '''select COLUMN_NAME from information_schema.columns where table_name=\'{table}\''''.format( table=sql_tupple[TABLE_NAME] )

    cursor = conn.cursor()
    cursor.execute( column_sql ) 
    columns = cursor.fetchall()
    cursor.close()
    columns = [c[0] for c in columns]
    column_names = ','.join(columns)

    select_stmt = '''select {columns} from {table}'''.format(
        columns=column_names,
        table=sql_tupple[TABLE_NAME])

    return ( select_stmt, columns, column_names )
    

def waypoint_extension(conn,sql_tupple):

    # Get all of the route waypoints
    select_stmt, columns, column_names = resolve_none_defaults(conn,sql_tupple)
    cursor = conn.cursor()
    cursor.execute( select_stmt )
    wps = cursor.fetchall()
    cursor.close()

    # Separate into VORs and RNAV waypoints
    vors = [v for v in wps if v[columns.index('fix_section_code')] == 'D']
    wps = [v for v in wps if v[columns.index('fix_section_code')] == 'E']

    intersections = []
    err=(0.001,
         0.001)
    # Loop through and find the ones that are within the err distance
    for v in vors:
        for w in wps:
            if (fabs(v[columns.index('longitude')] - \
                    w[columns.index('longitude')]) <= err[0] \
            and \
                fabs(v[columns.index('latitude')] - \
                      w[columns.index('latitude')]) <= err[1]) \
            and \
                (fabs(v[columns.index('longitude')] - \
                      w[columns.index('longitude')]) > 0.000001 \
            and \
                 fabs(v[columns.index('latitude')] - \
                      w[columns.index('latitude')]) >  0.000001):
                intersections.append([v,w])
    # Finally, get the uniques routes that have RNAV and VORS coincident.
    unique_intersections=[]
    routes=[]
    for v,w in intersections:
        rnav_point = [w[columns.index('route_id')],
                      w[columns.index('fix_id')]]
        if rnav_point not in routes:
            routes.append(rnav_point)
            unique_intersections.append([v,w])
            '''
            print(w[columns.index('route_id')],
              w[columns.index('fix_id')],
              w[columns.index('sequence')],
              '->',
              v[columns.index('route_id')],
              v[columns.index('fix_id')])
            '''
            
    table = sql_tupple[TABLE_NAME]
    sql = 'INSERT INTO {table}({columns}) VALUES({values});'
    # Now we update the AIRWAY table. I'll add the VOR into the sequence
    for v,w in unique_intersections:
        v=list(v)
        w=list(w)
        sequence = w[columns.index('sequence')]
        sequence = sequence + 1
        rnav_route_id = w[columns.index('route_id')]
        v[columns.index('sequence')] = sequence
        v[columns.index('route_id')] = rnav_route_id
        cursor.close()
        cursor = conn.cursor()
        cursor.execute( sql.format(table=sql_tupple[TABLE_NAME],
                          columns=column_names[3:], # Remove the id
                          values=create_insert(v[1:]))) # and the id item
        cursor.close()
    conn.commit()
        
ETL_QUERIES={
    'AIRWAYS':(
        'airway',
        None, # Select statement
        None, # Column indexes
        waypoint_extension
    )
}
