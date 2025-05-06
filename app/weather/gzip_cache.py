
from io import BytesIO
import gzip, json
import requests

class GzipCache:
    def __init__(self,remote_file,local_file,no_cache=True):
        print(remote_file)
        response = requests.get(remote_file)
        self.unzipped_data = None
        if response.status_code == 200:
            if no_cache:
                of = BytesIO()
                of.write(response.content)
                self.unzipped_data = gzip.decompress(of.getbuffer())
            else:
                with open(local_file, mode="wb") as of:
                    of.write(response.content)
                with gzip.open(local_file, 'rb') as inf:
                    self.unzipped_data  = inf.read()

        else:
            print('Could not update internet file.....')


            
    def get_data(self):
        return self.unzipped_data

    def get_json_data(self):
        return json.loads(self.get_data())
 
