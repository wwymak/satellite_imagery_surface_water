# script to get rgb imagery from https://s2maps.eu/
from urllib.request import urlretrieve
from pathlib import Path
from joblib import Parallel, delayed
import time
from tqdm import tqdm
import numpy as np
import requests
import shutil

lake_to_bounding_box_map = {
    'poopo_bolivia':(-68.66848367000537,-19.687928531849003,-66.67924128546656,-17.8774477409051),
    'urmia_iran':(44.587725529095295,36.86436828406643,46.230181583782795,38.50682433875393),
    'mead_mojave_usa':(115.42507235769445,34.94273489926993,-113.78261630300695,36.58519095395743),
    'aral_sea':(58.032853536637845,43.955292007325,61.317765646012845,47.2402041167),
    'copais_lake_greece':(23.214268551013436,38.36067354565393,23.350911007068124,38.4633270490719),
    'ramganga_india':(78.63716910452058,29.468167756293038,78.91045401662996,29.673474763128976),
    'qinhai_china':(99.56471967977474,35.70094613663666,101.20168257039974,37.34340219132416),
    'salton_sea_us':(-116.21928854749297,32.903320741965295,-115.40080710218047,33.724548769309045),
    'faguibine_mali':(-4.656089323623854,14.959306189862815,-3.0191264329988536,16.601762244550315),
    'mono_usa':(-119.22357779576633,37.797192162208084,-118.81433707311008,38.20780617587996),
    'walker_usa':(-118.82841344222616,38.58649115903216,-118.62379308089804,38.791798165868094),
    'balaton_hungary':(17.138306471163226,46.438781725159295,18.231446119600726,47.260009752503045),
    'koroenia_greece':(23.34167375183668,40.56321556296156,23.614958663946055,40.7685225697975),
    'salda_turkey':(29.6337346568769,37.49763563391751,29.736044837540963,37.60028913733548),
    'burdur_turkey':(30.008970333642345,37.6345355820376,30.373579098290783,37.83984258887354),
    'menocino_usa':(-123.19613698824355,39.189371563341254,-123.14498189791152,39.24069831505024),
    'elephant_butte_reservoir_usa':(-107.23803910498334,33.14614806405013,-107.13572892431928,33.2488015674681),
}

def construct_s2cloudless_image_url(minx, miny, maxx, maxy, layer):
    BASE_URL = "https://tiles.maps.eox.at/wms?service=wms&request=getmap&version=1.1.1"
    LAYER = "s2cloudless-2019"
    WIDTH = 4096
    HEIGHT = 4096
    CRS = "epsg:4326"

    return f"{BASE_URL}&layers={layer}&bbox={minx},{miny},{maxx},{maxy}&width={WIDTH}&height={HEIGHT}&srs={CRS}"


def download_s2cloudless_for_location_all_layers(minx, miny, maxx, maxy, lake_name, output_data_directory):
    layers = ["s2cloudless-2019","s2cloudless-2018","s2cloudless"]
    urls = [construct_s2cloudless_image_url(minx, miny, maxx, maxy, layer) for layer in layers]
    filenames = [f"{lake_name}_{np.floor(minx)}_{np.floor(miny)}_{np.floor(maxx)}_{np.floor(maxy)}_{layer}.jpg" for layer in layers]
    
    for url, filename in list(zip(urls, filenames)):
        # urlretrieve(url, Path(output_data_directory)/filename)

        r = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
    
            # Open a local file with wb ( write binary ) permission.
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, Path(output_data_directory)/f)

        else:
            print('Image err ', url)


if __name__ == "__main__":
    loop_items = []
    for lake, bounding_box in tqdm(lake_to_bounding_box_map.items()):
        minx, miny, maxx, maxy = bounding_box
        download_s2cloudless_for_location_all_layers(minx, miny, maxx, maxy, lake,Path("/media/wwymak/Storage/surface_water_changes_satellite_data/s2cloudless"))
        time.sleep(20)
        # loop_items.append((minx, miny, maxx, maxy, lake))
    # Parallel(n_jobs=12, prefer='threads')(delayed(download_s2cloudless_for_location_all_layers)(
    #     minx, miny, maxx, maxy, lake,Path("/media/wwymak/Storage/surface_water_changes_satellite_data/s2cloudless")
    # ) for minx, miny, maxx, maxy, lake in tqdm(loop_items))
