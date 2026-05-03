import json
import os
from collections import namedtuple
from urllib import parse
from concurrent.futures import ThreadPoolExecutor

import requests


CACHE_KEY = 'AAICampusAPICacheKey'

SearchResult = namedtuple('SearchResult', ['staff', 'rooms', 'organizations'])


class AauRoomsApi:
    """
    Wrapper for AAU API
    """
    API_PROTOCOL = 'https'
    API_DOMAIN = 'campus.aau.at'

    ROOMS_SEARCH_PATH = '/cgis/aau-api/search/rooms'

    AAU_CLIENT_ID = os.getenv('AAU_CLIENT_ID')
    AAU_CLIENT_SECRET = os.getenv('AAU_CLIENT_SECRET')

    def __init__(self, client_id=AAU_CLIENT_ID,
                 client_secret=AAU_CLIENT_SECRET):

        self.client_id = client_id
        self.client_secret = client_secret


    def get_and_save_access_token(self):
        """
        Requests and saves in cache access_token. Cache duration is equal to
        access_token expiry period.
        :return: access_token value
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }

        url = parse.urlunsplit(('https',
                                'oauth2.aau.at',
                                'oauth/token',
                                parse.urlencode(data),
                                ''))

        response = requests.post(url)

        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json['access_token']
            expires_in = response_json['expires_in']
            # cache.set(CACHE_KEY, access_token, timeout=expires_in)
            return access_token
        else:
            return

    @property
    def access_token(self):
        """
        Returns access_token, either be it from cache or acquired just now
        :return: access_token value
        """
        # at = cache.get(CACHE_KEY)
        at = None

        if at is None:
            at = self.get_and_save_access_token()

            if at:
                return at
            else:
                return None
        return at

    def build_url(self, path, query_data=None):
        """
        Utility function. Constructs full url to access API methods
        :param path: path to specific method
        :param query_data: dictionary of query paramerets
        :return: URL string
        """
        query_data = query_data or {}
        url = parse.urlunsplit((self.API_PROTOCOL,
                                self.API_DOMAIN,
                                path,
                                parse.urlencode(query_data),
                                ''))
        return url

    def get_all_rooms(self):

        data = {'access_token': self.access_token}

        res = requests.get(self.build_url(self.ROOMS_SEARCH_PATH, data))

        if res.status_code == 200:

            fa = res.json()

            if fa:
                return res.json()
            else:
                return None
        else:
            return {"error": "no data found", "method": "search_rooms"}

