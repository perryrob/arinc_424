# find_route

from .feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES

def distance_crs( conn, fixes );
'''
Assume VORs are 3 letters airports 4 letters and waypoints 5 leters
'''

for fix in fixes:

    if len(fix) == 3:
        sql = FEATURE_SQL_QUERIES['VORS'][FEATURE_SQL]
        values = FEATURE_SQL_QUERIES['VORS'][FEATURE_VALUES]
