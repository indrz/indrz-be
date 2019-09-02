import os
from collections import namedtuple
from urllib import parse
from concurrent.futures import ThreadPoolExecutor


import requests
from django.core.cache import cache

aau_client_id = os.getenv('aau_client_id')
aau_client_secret = os.getenv('aau_client_secret')

CACHE_KEY = 'AAICampusAPICacheKey'

SearchResult = namedtuple('SearchResult', ['staff', 'rooms', 'organizations'])


class AAICampusAPI:
    """
    Wrapper for AAU API
    """
    API_PROTOCOL = 'https'
    API_DOMAIN = 'campus-api.aau.at'
    OAUTH_TOKEN_PATH = '/oauth/token'
    STAFF_SEARCH_PATH = '/v1/cgis/search/staff'
    ROOMS_SEARCH_PATH = '/v1/cgis/search/rooms'
    ORGANIZATIONS_SEARCH_PATH = '/v1/cgis/search/ou'

    def __init__(self, client_id=aau_client_id,
                 client_secret=aau_client_secret):

        self.client_id = client_id
        self.client_secret = client_secret

    def filter_no_roomkey(self, data, source):

        newres = []

        for result in data:
            if 'rooms' in result:
                if result['rooms']:
                    if len(result['rooms']) > 1:
                        name = result['firstname'] + " " + result['lastname']
                        # one user can be assigned to multiple rooms, take first one
                        res = {'name': name, 'roomcode': result['rooms'][0], "src": source}
                        newres.append(res)
                    elif len(result['rooms']) == 1:
                        name = result['firstname'] + " " + result['lastname']
                        # one user can be assigned to multiple rooms, take first one
                        res = {'name': name, 'roomcode': result['rooms'][0], "src": source}
                        newres.append(res)
                    else:
                        continue

                else:
                    continue
            elif 'roomcode' in result:
                if result['roomcode']:
                    # rooms search found somethin in aau api call
                    name = result['roomcode']
                    res = {'name': name, 'roomcode': result['roomcode'], "category_de": result['category_de'], "src": source}
                    newres.append(res)
                else:
                    continue
            elif 'raum_code' in result:
                if result['raum_code']:
                    # rooms search found somethin in aau api call
                    name = result['name']
                    homepage = ""
                    if 'homepage' in result:
                        homepage = result['homepage']
                    res = {'name': name, 'roomcode': result['raum_code'], "src": source, "homepage": homepage}
                    newres.append(res)
                else:
                    continue

        if newres:
            return newres
        else:
            return []

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

        response = requests.get(self.build_url(self.OAUTH_TOKEN_PATH, data))

        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json['access_token']
            expires_in = response_json['expires_in']
            access_token = response_json['access_token']

            cache.set(CACHE_KEY, access_token, timeout=expires_in)
            return access_token
        else:
            return

    @property
    def access_token(self):
        """
        Returns access_token, either be it from cache or acquired just now
        :return: access_token value
        """
        at = cache.get(CACHE_KEY)
        if at is None:
            at = self.get_and_save_access_token()

            if at:
                return at
            else:
                return None
        return at

    def search_staff(self, name):
        """
        Searches for staff by name
        :param name:
        :return: list of dicts
        """
        data = {
            'access_token': self.access_token,
            'name': name
        }

        res = requests.get(self.build_url(self.STAFF_SEARCH_PATH, data))

        if res.status_code == 200:

            res_json = res.json()

            people_with_rooms_assigned = self.filter_no_roomkey(res_json, source="external person api")
            if people_with_rooms_assigned:
                return people_with_rooms_assigned
            else:
                return None
                # return {"error": "no room assigned", "method": "search_staff"}
        else:
            return None
            # return {"error": "no data found", "method": "search_staff"}

    def search_staff_unmodified(self, name):
        """
        Searches for staff by name
        :param name:
        :return: list of dicts
        """
        data = {
            'access_token': self.access_token,
            'name': name
        }

        res = requests.get(self.build_url(self.STAFF_SEARCH_PATH, data))

        if res.status_code == 200:
            return res.json()
        else:
            return None
            # return {"error": "no data found", "method": "search_staff"}


    def search_rooms(self, *, room_id=None, room_number=None, description=None,
                     ou=None):
        """
        Searches for rooms by either room ID
        or room number
        or description
        or organization

        Arguments are mutually exclusive
        :param room_id:
        :param room_number:
        :param description:
        :param ou:
        :return: list of dicts
        """

        if room_id:
            url = '%s/%s' % (self.ROOMS_SEARCH_PATH, room_id)
            return requests.get(self.build_url(url)).json()

        data = {'access_token': self.access_token}
        for key, value in (('roomnumber', room_number),
                           ('description', description),
                           ('ou', ou)):
            if value:
                data[key] = value

        res = requests.get(self.build_url(self.ROOMS_SEARCH_PATH, data))

        if res.status_code == 200:

            fa = self.filter_no_roomkey(res.json(), source="external rooms api")

            if fa:
                return fa
            else:
                return None
        else:
            return None
            # return {"error": "no data found", "method": "search_rooms"}

    def search_rooms_simple(self, name):
        """
        Simplified version of self.search_rooms() for usage in
        ThreadPoolExecutor.

        Accepts single argument `name` that is passed as `description` argument
        to self.search_rooms()
        :param name:
        :return: list of dicts
        """
        return self.search_rooms(description=name)

    def search_organizations(self, name):
        """
        Searches for organization by name
        :param name:
        :return: list of dicts
        """

        data = {
            'access_token': self.access_token,
            'name': name
        }

        res = requests.get(self.build_url(self.ORGANIZATIONS_SEARCH_PATH,
                                           data))

        if res.status_code == 200:

            fa = self.filter_no_roomkey(res.json(), source="external organization api")

            if fa:
                return fa
            else:
                return None
        else:
            return None
            # return {"error": "no data found", "method": "search_organizations"}


    def search(self, name):
        """
        Searches for staff, rooms and organizations at the same time.
        Returns SearchResult named tuple with three result sets
        :param name:
        :return:
        """
        pool = ThreadPoolExecutor(3)
        funcs = (self.search_staff,
                 self.search_rooms_simple,
                 self.search_organizations)
        futures = [pool.submit(func, name) for func in funcs]

        aau_api_search = SearchResult(*[future.result() for future in futures])

        if any(aau_api_search):
            return aau_api_search
        else:
            return None



def aau_api_res_source(x):
    result_type = ''

    if x.rooms:
        result_type = 'rooms'
        return result_type
    elif x.staff:
        result_type = 'staff'
        return result_type
    elif x.organizations:
        result_type = 'organizations'
        return result_type
    else:
        return None


