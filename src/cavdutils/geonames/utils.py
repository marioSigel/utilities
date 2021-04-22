
import requests
import pandas as pd
from geopy import Point

GEONAMES_URL = 'http://api.geonames.org'


def query_geonames(company_name, google):
    company_name = company_name.lower()
    addresses = {}
    codes = ['MFG', 'FCL', 'TOWR']  # codes from https://www.geonames.org/export/codes.html
    for c in codes:
        res = requests.get(GEONAMES_URL + '/searchJSON?q={}&featureCode={}&username={}'.format(
            company_name,
            c,
            'test_app'
        ))

        res = res.json()['geonames']
        res = {x['geonameId']: x for x in res}

        addresses.update(res)

    addresses = {k: v for k, v in addresses.items() if any(
        [company_name in (v.get(field).lower() or '') for field in ['name', 'toponymName']])
                 }

    if not addresses:
        return None

    keys = sorted(addresses[list(addresses.keys())[0]].keys())
    addresses = pd.DataFrame([[addresses[_id].get(k) for k in keys]
                              for _id in addresses],
                             columns=keys)

    addresses = addresses.assign(
        address=addresses.lat.combine(addresses.lng, lambda lat, lon: google.reverse(Point(lat, lon)).address),
        source='places_apis'
    )

    return addresses
