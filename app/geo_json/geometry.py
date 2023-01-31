from math import pi, sin, cos, asin, acos, atan2, fmod

EARTH_RADIUS = 6371.0 * 1000.0 # meters

def NM_to_meters( nm ):
    return 1852.0 * nm

def deg_to_rad( deg ):
    return deg * pi / 180.0

def rad_to_deg( rad ):
    ret_val = rad * 180.0 / pi
    return ret_val

def dis_to_radians( nm ):
    return (pi/(180*60))*nm

def lat_from_center_dis( lat_rad, tc_rad, d_rad ):
    return asin(sin(lat_rad)*cos(d_rad)+cos(lat_rad)*sin(d_rad)*cos(tc_rad))

def lon_from_center_dis( lon_rad, lat_rad, projected_lat_rad, tc_rad, d_rad ):
    dlon=-atan2(sin(tc_rad)*sin(d_rad)*cos(lat_rad),
               cos(d_rad)-sin(lat_rad)*sin(projected_lat_rad))
    return fmod( lon_rad-dlon +pi,2*pi ) - pi   

def point_project( center_deg=(0,0), angle_deg=0, radius_nm=1):

    tc = deg_to_rad(angle_deg)
    lon1 = deg_to_rad(center_deg[0])
    lat1 = deg_to_rad(center_deg[1])
    d = dis_to_radians(radius_nm)

    lat = lat_from_center_dis( lat1, tc, d )
    lon = lon_from_center_dis( lon1, lat1, lat, tc, d )

    return ( rad_to_deg(lon), rad_to_deg(lat) )

def  circle_center_polygon( radius_nm=1, segments=36, center_deg=(0,0),
                     variation_deg=0 ):

    tc = variation_deg
    increment_deg = 360 / segments
    lat1 = center_deg[1]
    lon1 = center_deg[0]
    d = radius_nm

    ret_val=[]
    for seg in range(0,segments+1):
        end_deg = tc + increment_deg    
        ret_val.append( point_project( (lon1,lat1), tc, d ) )
        tc = end_deg
        
    return [ret_val]


def line_center_angle( radius_nm=1, center_deg=(0,0), angle_deg=0 ):

    angle = angle_deg
    lon1 = center_deg[0]
    lat1 = center_deg[1]
    d = radius_nm

    lon_lat = point_project( (lon1,lat1), angle, d )

    return [(lon1,lat1),
            (lon_lat[0],lon_lat[1])]

def true_course_deg(p1_deg=(0,0),p2_deg=(1,1), make_360=False):

    lon1 = deg_to_rad(p1_deg[0]) * -1.0
    lat1 = deg_to_rad(p1_deg[1])

    lon2 = deg_to_rad(p2_deg[0]) * -1.0
    lat2 = deg_to_rad(p2_deg[1])

    tc =  rad_to_deg(
        fmod(atan2(sin(lon1-lon2)*cos(lat2),
                   cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon1-lon2)),
             2.0*pi))

    if make_360 and tc < 0:
        return 360 + tc

    return tc

if __name__ == '__main__':
    # TUS to SSO should be 71 degrees
    # SSO to TUS should be 250 degrees
    tc = true_course_deg((-110.9148,32.0952),(-109.2631,32.2692) ,True)
    print('rad ', deg_to_rad(tc))
    print( tc  -12 )
    tc = true_course_deg((-109.2631,32.2692),(-110.9148,32.0952) ,True)
    print('rad ', deg_to_rad(tc))
    print( tc  -13 )
    print('================================')
    p1 = (0,0)
    for i in range(0,9):
        p2 = (sin(deg_to_rad( i*45 )),cos(deg_to_rad( i*45 )))        

        tc_1 =  true_course_deg(p1, p2 ,True)
        tc_2 =  true_course_deg(p2, p1 ,True)

        pp2 = point_project( p1, tc_1, 60) # Gotta have 60 for unity

        print('i   tc1  tc2    p2                 pp2' )
        print('==================================================')
        print(i,tc_1,tc_2,p2,pp2)
