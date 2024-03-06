
from bs4 import BeautifulSoup as BS
from urllib import request
import requests
import zipfile,gzip
import io
import os, shutil

CIFP_URL='https://aeronav.faa.gov/Upload_313-d/cifp'
WEATHER_BASE_CACHE='https://aviationweather.gov/data/cache/'

TMP_SAVE_PATH='app/cifp'
WEATHER_SAVE_PATH='app/aviation_weather'

METAR_CACHE ='metars.cache.csv.gz'
TAF_CACHE='tafs.cache.csv.gz'
AIRSIGMET_CACHE='airsigmets.cache.csv.gz'
PIREP_CACHE='aircraftreports.cache.csv.gz'
STATIONS_CACHE='stations.cache.json.gz'

WEATHER_PRODUCTS=[
    METAR_CACHE,
    TAF_CACHE,
    AIRSIGMET_CACHE,
    PIREP_CACHE,
    STATIONS_CACHE
]


def clean_dir(a_dir):

    folder = a_dir
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if filename.find('keep') != -1: continue
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def update_cifp():
    clean_dir( TMP_SAVE_PATH )
    data_page = request.urlopen(CIFP_URL).read()
    soup = BS(data_page,'html.parser')
    ############################################################
    # Get the latest update
    latest_update = soup.find_all('a')[-1:][0].attrs['href'].split('/')[-1:][0]
    r = requests.get(CIFP_URL+'/'+latest_update, stream=True)
    in_mem_file = io.BytesIO(r.content)

    zip_file = zipfile.ZipFile(in_mem_file)

    zip_file.extractall(TMP_SAVE_PATH)

def update_weather():
    clean_dir(WEATHER_SAVE_PATH)
    for weather_product in WEATHER_PRODUCTS:
        r = requests.get(WEATHER_BASE_CACHE+weather_product, stream=True)

        in_mem_file = io.BytesIO(r.content)
        
        zip_file = gzip.GzipFile(fileobj=in_mem_file)

        with io.TextIOWrapper(zip_file, encoding='utf-8') as decoder:
            content = decoder.read()
            with open(WEATHER_SAVE_PATH+'/'+'.'.join(weather_product.split('.')[:-1]),'w') as f:
                f.write(content)
        
update_cifp()
update_weather()
