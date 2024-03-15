


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

    def get_json(self):
        with open( self.input_file, 'r') as inf:
            pos = -1
            self.json = []
            for line in inf.readlines():
                pos += 1
                if pos > self.start_pos:
                    line = line.strip()
                    data_cols = line.split(',')
                    for i in range(0,len(self.columns)):
                        self.json.append(
                            {
                                self.colums[i]:data_cols[i].strip() }
                            )
                    break
        return self.json
                
if __name__ == '__main__':
    ctj = Csv_to_JSON()
    ctj.get_json()
