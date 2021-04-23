import requests
import pandas as pd

URL = 'https://discover.search.hereapi.com/v1/discover'

keywords = ['factory', 'plant', 'facility', 'headquarter', 'office', 'gate',
            'assembly', 'supply', 'supplier', 'manufacturing', 'business']
excluded_categories = ['Automobile Dealership - New Cars',
                       'Car Repair',
                       'Auto Parts',
                       'Police Station',
                       'Park-Recreation Area',
                       'Specialty Store',
                       'City Hall']


def fetch(coord, brand, keyword, here_apikey):
    res =  requests.get(URL + '?q={}&at={}&lang=en-US&apiKey={}'.format(
        '{}+{}'.format(brand, keyword),
        coord,
        here_apikey))
    return res.json()


def query_here(company_name, here_apikey, lat, lng, additional_keywords=None):
    all_res = {}
    coord = f'{lat},{lng}'

    _keywords = keywords + (additional_keywords or [])

    for keyword in _keywords:
        items = {i['id']: i for i in (fetch(coord, company_name, keyword, here_apikey) or {'items': []})['items']}
        all_res.update(items)

    all_res_filtered = [item for item in all_res.values() if (
            not any([
                any([i['name'] == cat for cat in excluded_categories])
                for i in item.get('categories', [])])
            and (
                company_name.lower() in item.get('title', '').lower() or
                company_name.lower() in item.get('address', {}).get('label', '').lower())
            )]

    addresses = pd.DataFrame(
        [[r['title'], r['address']['label'], r['position']['lat'], r['position']['lng']] for r in all_res_filtered],
        columns=['name', 'address', 'lat', 'lng'])

    addresses = addresses.assign(
        source='places_apis'
    )

    return addresses
