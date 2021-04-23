from googlemaps import Client
import pandas as pd


def query_google(company_name, google_apikey, country_codes=None, additional_keywords=None):
    additional_keywords = ['plant'] if additional_keywords is None else additional_keywords
    google_maps = Client(key=google_apikey)

    if country_codes is None:
        raise Exception("""
        List of ISO 3166-1 alpha-2 country codes required, e.g. country_code_list=['DE']. 
        See https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 for codes.""")

    all_res = []

    for cc in country_codes:
        country_res = google_maps.places(' '.join([company_name] + additional_keywords), region=cc).get('results')
        if country_res:
            all_res += [r for r in country_res if
                        any(
                            [company_name.lower() in r.get(f, '').lower() for f in ['formatted_address', 'name']]) and
                        not any(
                            [term in r.get('formatted_address', '').lower() for term in
                                [f'near {company_name}', f'behind {company_name}']])]

    all_res = [r for r in all_res if not any([tag in r['types'] for tag in ['car_dealer', 'car_repair', 'store']])]

    addresses = pd.DataFrame([[d['name'],
                               d['formatted_address'],
                               d['geometry']['location']['lat'],
                               d['geometry']['location']['lng']]
                               for d in all_res], columns=['name', 'address', 'lat', 'lng'])

    addresses = addresses.assign(
        source='places_apis'
    )

    return addresses
