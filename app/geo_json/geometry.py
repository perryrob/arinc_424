from math import pi, sin, cos, asin, acos, atan2, fmod

EARTH_RADIUS = 6371.0 * 1000.0 # meters

def NM_to_meters( nm ):
    return 1852.0 * nm

def deg_to_rad( deg ):
    return deg * pi / 180.0

def rad_to_deg( rad ):
    return rad * 180.0 / pi


def dis_to_radians( nm ):
    return (pi/(180*60))*nm

def lat_from_center_dis( lat_rad, tc_rad, d_rad ):
    return asin(sin(lat_rad)*cos(d_rad)+cos(lat_rad)*sin(d_rad)*cos(tc_rad))

def lon_from_center_dis( lon_rad, lat_rad, projected_lat_rad, tc_rad, d_rad ):
    dlon=atan2(sin(tc_rad)*sin(d_rad)*cos(lat_rad),
               cos(d_rad)-sin(lat_rad)*sin(projected_lat_rad))
    return fmod( lon_rad-dlon +pi,2*pi )-pi   


def  circle_center_polygon( radius_nm=1, segments=36, center_deg=(0,0),
                     variation_deg=0 ):

    tc = deg_to_rad(variation_deg)
    increment_rad = deg_to_rad(360) / segments
    ret_val=[]
    lat1 = deg_to_rad(center_deg[1])
    lon1 = deg_to_rad(center_deg[0])
    d = dis_to_radians(radius_nm)
    for seg in range(0,segments+1):
        end_rad = tc + increment_rad    

        lat = lat_from_center_dis( lat1, tc, d )
        lon = lon_from_center_dis( lon1, lat1, lat, tc, d )

        ret_val.append((rad_to_deg(lon),rad_to_deg( lat) ))
        tc = end_rad
    return [ret_val]

def line_center_angle( radius_nm=1, center_deg=(0,0), variation_deg=0 ):

    angle =  deg_to_rad(variation_deg)
    lat1 = deg_to_rad(center_deg[1])
    lon1 = deg_to_rad(center_deg[0])
    d = dis_to_radians(radius_nm)
    
    lat = lat_from_center_dis( lat1, angle, d )
    lon = lon_from_center_dis( lon1, lat1, lat, angle, d )

    return [(rad_to_deg(lon1),rad_to_deg(lat1)),
            (rad_to_deg(lon),rad_to_deg(lat))]

