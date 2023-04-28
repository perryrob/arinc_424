
from bs4 import BeautifulSoup as BS
from urllib import request

WIND_DATA_URL='https://aviationweather.gov/windtemp/data'
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
    def __init__(self, time=6):

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
            (0,3,'noop'),
            (4,8,'wind3k'),
            (9,16,'wind624k'),
            (17,24,'wind624k'),
            (25,32,'wind624k'),
            (33,40,'wind624k'),
            (41,48,'wind624k'),
            (49,55,'wind30k'),
            (56,62,'wind30k'),
            (56,62,'wind30k')
        ]

        self.wind_data={}
        
        self.get_wind(
            level='low',region='all',layout='off',time=str(time))
        
    def _parse_wind_line(self,data_line):
        station = data_line[ self.TOKENS[0][0]:
                             self.TOKENS[0][1]]
        self.wind_data[station] = []
        for token_idx in self.TOKENS[1:]:
            # print('|'+data_line[token[0]:token[1]]+'|')
            tok = data_line[token_idx[0]:token_idx[1]]
            func = getattr(F,token_idx[2])
            self.wind_data[station].append(func(tok))

            
    def get_wind(self,**kwargs):
        # Build up the args
        args='?'
        for k in kwargs.keys():
            args = args + k + '=' + kwargs[k] + '&'
        args = args[:-1]
    
        data_page = request.urlopen(WIND_DATA_URL + args).read()

        soup = BS(data_page,'html.parser')
        for data in soup.findAll('pre'):
            counter = 0
            for line in data.text.split('\n'):
                counter=counter+1
                if len(line.strip()) ==0 : continue                           
                if counter > self.DATA_STARTS_AFTER:
                     self._parse_wind_line(line)
                else:
                    # print(line)
                    pass
                    
if __name__ == '__main__':
    w = Wind()
   
    
