from urllib import parse
import os
import pytest
from django.test import Client, TestCase, RequestFactory, SimpleTestCase
from django.conf import settings

from homepage.aau_campus_api import AAICampusAPI



import requests, json
import pprint

aau_client_id = os.getenv('aau_client_id')
aau_client_secret = os.getenv('aau_client_secret')


class TestAAICampusAPI(TestCase):

    def setup(self):
        self.client_id = aau_client_id
        self.client_secret = aau_client_secret
        self.API_PROTOCOL = 'https'
        self.API_DOMAIN = 'campus-api.aau.at'
        self.OAUTH_TOKEN_PATH = '/oauth/token'
        self.STAFF_SEARCH_PATH = '/v1/cgis/search/staff'
        self.ROOMS_SEARCH_PATH = '/v1/cgis/search/rooms'
        self.ORGANIZATIONS_SEARCH_PATH = '/v1/cgis/search/ou'

    def test_get_save_access_token(self):
        self.setup()
        s = requests.session()

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }
        url = parse.urlunsplit((self.API_PROTOCOL,
                                self.API_DOMAIN,
                                self.OAUTH_TOKEN_PATH,
                                parse.urlencode(data),
                                ''))

        response = s.get(url)

        response_json = response.json()
        access_token = response_json['access_token']
        expires_in = response_json['expires_in']

        self.token = "a72fb464-2285-4045-b63d-e88521d3e017"
        assert access_token == self.token

    def test_access_token(self):
        auth_url = "https://campus-api.aau.at/oauth/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(
            aau_client_id, aau_client_secret)
        auth_resp = s.get(auth_url)

        self.access_token = auth_resp.json()['access_token']
        print(self.access_token)

        assert auth_resp.status_code == 200

        if auth_resp.status_code == 200:
            assert auth_resp.json()['access_token']

    def test_get_all_aau_rooms(self):
        self.setUp()
        url = parse.urlunsplit((self.API_PROTOCOL,
                                self.API_DOMAIN,
                                path,
                                parse.urlencode(query_data),
                                ''))

        s = requests.session()
        auth_url = "https://campus-api.aau.at/oauth/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(
            aau_client_id, aau_client_secret)
        auth_resp = s.get(auth_url)

        print(auth_resp.content)

        access_token = auth_resp.json()['access_token']
        token = "a72fb464-2285-4045-b63d-e88521d3e017"

        assert access_token == token

        resp_all_rooms = s.get('https://campus-api.aau.at/v1/cgis/search/rooms&access_token={0}'.format(token))
        all_rooms = resp_all_rooms.json()
        with open('all_rooms.json', 'w') as f:
            for room in all_rooms:
                f.write(str(all_rooms))
        #
        # for k,v in all_rooms[0]:
        #     print(k,v)
        # assert len(all_rooms) < 1


def test_get_save_access_token():
    my_token = AAICampusAPI().get_and_save_access_token()
    assert my_token is not None


def test_search_aau_api_staff():
    x = AAICampusAPI().search("Martin Swaton")
    assert "roomcode" in x.staff[0]
    assert "name" in x.staff[0]
    assert "src" in x.staff[0]
    if "src" in x.staff[0]:
        assert x.staff[0]['src'] == "external person api"


def test_search_aau_api_rooms_simple():
    x = AAICampusAPI().search('Z.2.13a')
    room_expected = [{'buildingcolor': None,
                      'buildingname': 'Hauptgebäude, Zentraltrakt',
                      'capacity': 2,
                      'category_de': 'Personalraum',
                      'category_en': None,
                      'fancyname_de': None,
                      'fancyname_en': None,
                      'floorname': 'Ebene 2',
                      'pk_big': None,
                      'roomcode': 'Z.2.13a',
                      'roomname_de': 'Z.2.13a',
                      'roomname_en': None,
                      'tid': None}]
    assert room_expected == x.rooms


def test_search_aau_api_organizations():
    x = AAICampusAPI().search('Abteilung für Server- und Kommunikationssysteme')
    has_keys = False
    if all(k in x.organizations for k in aau_org_api_keys):
        has_keys = True
    else:
        has_keys = False

    assert has_keys == True


def test_list_all_aau_rooms():
    x = AAICampusAPI().search_rooms()
    assert x is not None
    assert isinstance(x, list)
    assert len(x) > 1
    assert "category_de" in x[0]
    assert "name" in x[0]
    assert "src" in x[0]
    assert "roomcode" in x[0]
    assert len(x[0]) == 4
