import overpy

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


def query_osm(company_name, overpass_instances, instance_id):
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
        return query_osm(company_name, overpass_instances, instance_id)