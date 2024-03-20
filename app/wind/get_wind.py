
from urllib import request

from wind.feature_sql import FEATURE_SQL_QUERIES,FEATURE_SQL,FEATURE_VALUES

WIND_DATA_URL='https://aviationweather.gov/api/data/windtemp'
################################################################################
#
#  level = (low,high)
#  fcst = (6,12,24)
#  region = (all)
#  layout = off

class F:
    def noop(token):
        return token
    
    def wind3k(token):
        if token.isspace():
            return None

        vec = float(token[0:2]) * 10.0
        vel = float(token[2:4])

        if vec == 990:
            vec=0.0
            
        return (vec,vel)
        
    def wind624k(token):
        if token.isspace():
            return None

        tmp = None
        
        vec = float(token[0:2]) * 10.0
        vel = float(token[2:4])
        try:
            tmp = float(token[4:7])
        except:
            pass
        
        if vec == 990:
            vec=0.0
            
        return (vec,vel,tmp)
    
    def wind30k(token):
        if token.isspace():
            return None

        vec = float(token[0:2]) * 10.0
        vel = float(token[2:4])
        tmp = -float(token[4:6])
        
        if vec == 990:
            vec=0.0
            vel=0.0

        return (vec,vel,tmp)
    
class Wind:
    def __init__(self, time=6, conn = None):

        self.IGNORE=-9999
        
        self.DATA_STARTS_AFTER = 8
        # 000
        # FBUS31 KWNO 282000
        # FD1US1
        # DATA BASED ON 281800Z
        # VALID 290000Z   FOR USE 2000-0300Z. TEMPS NEG ABV 24000
        # FT  3000    6000    9000   12000   18000   24000  30000  34000  39000
        #123456789_123456789_1234567890_1234567890_1234567890_1234567890_12345
        #ABR 3315 3320-04 3221-09 3219-10 3225-23 3226-35 354147 354552 353853
        self.TOKENS=[
            (0,3,'noop',self.IGNORE),
            (4,8,'wind3k',3000),
            (9,16,'wind624k',6000),
            (17,24,'wind624k',9000),
            (25,32,'wind624k',12000),
            (33,40,'wind624k',18000),
            (41,48,'wind624k',24000),
            (49,55,'wind30k',30000),
            (56,62,'wind30k',34000),
            (56,62,'wind30k',39000)
        ]

        self.wind_data={}
        self.station_lon_lat={}
        
        self.get_wind(
            level='low',region='all',layout='off',fcst='06',date='')

        self.get_station_lon_lat(conn)

    def get_station_lon_lat(self,conn):
        if conn is None: return

        values = FEATURE_SQL_QUERIES['STATION'][FEATURE_VALUES]

        for station in self.wind_data.keys():
            sql = FEATURE_SQL_QUERIES['STATION'][FEATURE_SQL] % station
            cursor = conn.cursor()
            cursor.execute( sql )
            station = cursor.fetchall()
            cursor.close()
            try:
                point = [station[values['longitude']],
                         station[values['longitude']]]
                # print(point)
            except:
                pass
                # print(sql)
                

    def _interp_alt(self, alt):

        if alt > 39000 or alt < 3000:
            return (alt,None,None,None)
        
        alts = [t[3] for t in self.TOKENS[1:]]

        # [3000 - 39000]
        a1 = None
        a2 = None
        for a in alts:
            if alt == a:
                a2 = a
                a1 = 0
                return (alt,
                        alts.index(a),
                        alts.index(a),
                 1.0)
            elif alt < a and a2 is None:
                a2 = a
                a1= alts[alts.index(a)-1]

        return (alt,
                alts.index(a1),
                alts.index(a2),
                (alt-a1)/(a2-a1))

    def get_airdata(self,station,alt):
        
        a,idx1,idx2,interp = self._interp_alt(alt)

        if idx1 is None: return (alt,None,None,None)
        if idx2 is None: return (alt,None,None,None)

        try:
            airdata = self.wind_data[station]
            low_data = airdata[idx1][1]
            high_data = airdata[idx2][1]

            # print(low_data)
            # print(high_data)

            if low_data is None: return (alt,None,None,None)
            if high_data is None: return (alt,None,None,None)

            # vec,vel,tmp

            d_vec = high_data[0] - low_data[0]
            d_vel = high_data[1] - low_data[1]
            d_tmp = high_data[2] - low_data[2]

            r_vec = low_data[0] + d_vec * interp 
            if r_vec > 360:
                r_vec = r_vec - 360

            r_vel = low_data[1] + d_vel * interp
            r_tmp = low_data[2] + d_tmp * interp

            return (alt,r_vec,r_vel,r_tmp)
        except:
            (alt,None,None,None)
        
    def _parse_wind_line(self,data_line):
        station = data_line[ self.TOKENS[0][0]:
                             self.TOKENS[0][1]]
        self.wind_data[station] = []
        for token_idx in self.TOKENS[1:]:
            tok = data_line[token_idx[0]:token_idx[1]]
            func = getattr(F,token_idx[2])
            self.wind_data[station].append((token_idx[3],func(tok)))

        # Post process to remove missing data because of low altitude
        # Just copy down the higher values
        # If the last entry in the list is None (unlikely) this will break
        for i in range(0,len(self.wind_data[station])):
            if self.wind_data[station][i][1] is None:
                self.wind_data[station][i] = (self.wind_data[station][i][0],
                                              self.wind_data[station][i+1][1])
                
    def get_wind(self,**kwargs):
        # Build up the args
        args='?'
        for k in kwargs.keys():
            args = args + k + '=' + kwargs[k] + '&'
        args = args[:-1]

        # print(WIND_DATA_URL+args)
        
        data_page = request.urlopen(WIND_DATA_URL + args).read()
        data_page = data_page.decode('utf-8')
        counter = 0
        for line in data_page.split('\n'):
            counter=counter+1
            if len(line.strip()) ==0 : continue                           
            if counter > self.DATA_STARTS_AFTER:
                # if 'TUS' in line:
                    # print('FT  3000   6000   9000   12000    18000   24000  30000  34000  39000')
                    # print(line)
                self._parse_wind_line(line)
            else:                    
                pass
