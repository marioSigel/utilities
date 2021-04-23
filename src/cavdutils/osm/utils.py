import overpy
import pandas as pd
from geopy import Point
from cavdutils.map_services import get_geocoder

URL = 'https://overpass-api.de/api/interpreter'

overpass_urls = [
    'https://lz4.overpass-api.de/api/interpreter',
    'https://z.overpass-api.de/api/interpreter',
    'https://overpass.openstreetmap.ru/api/interpreter',
    'https://overpass.openstreetmap.fr/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.nchc.org.tw/api/interpreter'
]
overpass_instances = [overpy.Overpass(url=_url) for _url in overpass_urls]


def run_query(company_name, instance_id=0):
    try:
        return overpass_instances[instance_id].query("""
            [out:json];
            way["name"~"{0}",i]["industrial"];
            way["name"~"{0}",i]["landuse"="industrial"];
            out center;
            """.format(company_name))
    except:
        instance_id += 1
        if not instance_id < len(overpass_instances):
            raise Exception('Probably blocked by OSM due to too many requests.')
        return run_query(company_name, instance_id)


def query_osm(company_name, google_apikey):
    google = get_geocoder(google_apikey, 'google')

    res = run_query(company_name)

    addresses = pd.DataFrame([[w.tags['name'], w.center_lat, w.center_lon] for w in res.ways],
                                  columns=['name', 'lat', 'lng'])

    addresses = addresses.assign(
        address=addresses.lat.combine(addresses.lng, lambda lat, lng: google.reverse(Point(lat, lng)).address)
    )

    addresses = addresses.assign(
        source='places_apis'
    )

    return addresses
