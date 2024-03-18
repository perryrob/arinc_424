


class Csv_to_JSON:

    def __init__(self, input_file='app/aviation_weather/airsigmets.cache.csv'):
        self.input_file = input_file
        self.start_pos = -1
        with open( self.input_file, 'r') as inf:
            for line in inf.readlines():
                self.start_pos += 1
                if line.find(',') != -1:
                    line = line.strip()
                    raw_cols = line.split(',')
                    self.columns = raw_cols
                    break

        self.colums = [c.strip() for c in self.columns ]

        for i in range(0,len(self.colums)):
            if self.colums[i].find(':') > -1:                
                self.colums[i] = self.colums[i].replace(':','_')
                self.colums[i] = self.colums[i].replace(' ','_')

    def get_json(self):
        with open( self.input_file, 'r') as inf:
            pos = -1
            self.json = []
            for line in inf.readlines():
                pos += 1
                if pos > self.start_pos:
                    line = line.strip()
                    data_cols = line.split(',')
                    col_data_dict={}
                    for i in range(0,len(self.columns)):
                        if i >= len(data_cols):
                            print('warning less data than colums:',self.colums[i],'set to None')
                            col_data_dict[self.colums[i]] = None
                            continue
                        col_data_dict[self.colums[i]] = data_cols[i].strip()
                    self.json.append( col_data_dict )
        return self.json
                
if __name__ == '__main__':
    print(1)
    ctj = Csv_to_JSON( input_file='app/aviation_weather/airsigmets.cache.csv')    
    ctj.get_json()
    print(2)
    ctj = Csv_to_JSON( input_file='app/aviation_weather/aircraftreports.cache.csv')
    ctj.get_json()
    print(3)
    ctj = Csv_to_JSON( input_file='app/aviation_weather/metars.cache.csv')    
    ctj.get_json()
    print(4)
    ctj = Csv_to_JSON( input_file='app/aviation_weather/tafs.cache.csv')   
    ctj.get_json()

    
