
from geopy.geocoders import Here, Nominatim, GoogleV3
from geopy.extra.rate_limiter import RateLimiter


class RateLimitedGeocoder(object):
    def __init__(self, geolocator):
        self.geocode_func = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    def geocode(self, text):
        return self.geocode_func(text)


def get_geocoder(apikey, map_service='google'):
    if map_service == 'google':
        return GoogleV3(api_key=apikey)
    elif map_service == 'osm':
        _osm = Nominatim(user_agent="test_app")
        return RateLimitedGeocoder(_osm)
    elif map_service == 'here':
        return Here(apikey=apikey)

    raise Exception('Map service not supported')
