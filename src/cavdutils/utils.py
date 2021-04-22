import requests


GEONAMES_URL = 'http://api.geonames.org'


def query_geonames(company_name, page_addresses):
    codes = ['MFG', 'FCL', 'TOWR']  # codes from https://www.geonames.org/export/codes.html
    for c in codes:
        res = requests.get(GEONAMES_URL + '/searchJSON?q={}&featureCode={}&username={}'.format(
            company_name,
            c,
            'test_app'
        ))

        res = res.json()['geonames']
        res = {x['geonameId']: x for x in res}

        page_addresses.update(res)
