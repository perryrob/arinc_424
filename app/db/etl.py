
from math import fabs

TABLE_NAME=0
SELECT=1
COLUMNS=2
ETL_SCRIPT=3



def resolve_none_defaults( conn, sql_tupple ):
    column_sql = '''select COLUMN_NAME from information_schema.columns where table_name=\'{table}\''''.format( table=sql_tupple[TABLE_NAME] )

    cursor = conn.cursor()
    cursor.execute( column_sql ) 
    columns = cursor.fetchall()
    cursor.close()
    columns = [c[0] for c in columns]
    values = ','.join(columns)

    select_stmt = '''select {columns} from {table}'''.format(
        columns=values,
        table=sql_tupple[TABLE_NAME])

    return ( select_stmt, columns )
    

def waypoint_extension(conn,sql_tupple):

    select_stmt, columns = resolve_none_defaults(conn,sql_tupple)
    cursor = conn.cursor()
    cursor.execute( select_stmt )
    wps = cursor.fetchall()
    cursor.close()
    
    vors = [v for v in wps if v[columns.index('fix_section_code')] == 'D']
    wps = [v for v in wps if v[columns.index('fix_section_code')] == 'E']

    intersections = []
    err=(0.001,
         0.001)
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
                intersections.append((v,w))

    unique_intersections=[]
    routes=[]
    for v,w in intersections:
        if w[columns.index('route_id')] not in routes:
            routes.append(w[columns.index('route_id')])
            unique_intersections.append((v,w))
            print( w[columns.index('route_id')], '-',
                   w[columns.index('fix_id')], '|',
                   v[columns.index('route_id')], '-',
                   v[columns.index('fix_id')])


ETL_QUERIES={
    'AIRWAYS':(
        'airway',
        None, # Select statement
        None, # Column indexes
        waypoint_extension
    )
}
