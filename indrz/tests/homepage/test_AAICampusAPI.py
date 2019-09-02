from urllib import parse
import os
import pytest
from django.test import Client, TestCase, RequestFactory, SimpleTestCase
from django.conf import settings


db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_passwd = os.getenv('db_passwd')
db_database = os.getenv('db_name')
db_port = os.getenv('db_port')


aau_client_secret=  os.getenv('aau_client_secret')
aau_client_id = os.getenv('aau_client_id')

# from django.test import SimpleTestCase
from homepage.aau_campus_api import AAICampusAPI


import requests, json


settings.configure()

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "testdb",  # DB name
        'USER': "testrunner",  # DB user name
        'PASSWORD': db_pwd,  # DB user password
        'HOST': db_host,
        'PORT': db_port,
    }
}


class TestAAICampusAPI(SimpleTestCase):

    def setup(self,):
        self.client_id = aau_client_id
        self.client_secret = aau_client_secret
        self.API_PROTOCOL = 'https'
        self.API_DOMAIN = 'campus-api.aau.at'
        self.OAUTH_TOKEN_PATH = '/oauth/token'
        self.STAFF_SEARCH_PATH = '/v1/cgis/search/staff'
        self.ROOMS_SEARCH_PATH = '/v1/cgis/search/rooms'
        self.ORGANIZATIONS_SEARCH_PATH = '/v1/cgis/search/ou'


    def test_get_all_aau_rooms(self):

        one_room = {'buildingname': 'Hauptgebäude, Zentraltrakt', 'buildingcolor': None,
                    'capacity': None, 'category_de': 'Betriebs-technische Anlagen',
                    'category_en': None, 'fancyname_de': None, 'fancyname_en': None,
                    'floorname': 'Ebene 1', 'pk_big': None, 'roomcode': 'Z.1.10b',
                    'roomname_de': 'Projektionsraum', 'roomname_en': None, 'tid': 682}

        auth_url = "https://campus-api.aau.at/oauth/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(
            aau_client_id, aau_client_secret)

        s = requests.session()
        auth_resp = s.get(auth_url)

        assert auth_resp.status_code == 200

        access_token = auth_resp.json()['access_token']

        assert 'access_token' in auth_resp.json()

        resp_all_rooms = s.get('https://campus-api.aau.at/v1/cgis/search/rooms?&access_token={0}'.format(access_token))
        all_rooms = resp_all_rooms.json()

        assert 'buildingname' in all_rooms[0]

        assert len(all_rooms) > 2240  # current value is 2249 as of 1.1.2019

        # with open('all_rooms.json', 'w') as f:
        #     for room in all_rooms:
        #         f.write(str(room))


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
    room_expected = {'buildingcolor': None,
                      'buildingname': 'Hauptgebäude, Zentraltrakt',
                      'capacity': 2,
                      'category_de': 'Büroarbeit',
                      'category_en': None,
                      'fancyname_de': None,
                      'fancyname_en': None,
                      'floorname': 'Ebene 2',
                      'pk_big': None,
                      'roomcode': 'Z.2.13a',
                      'roomname_de': 'Z.2.13a',
                      'roomname_en': None,
                      'tid': None,
                     'name': 'Z.2.13a',
                     'src': 'external rooms api'
                     }

    # room_expected = """[{'name': 'Z.2.13a',
    # 'roomcode': 'Z.2.13a',
    # 'category_de': 'Büroarbeit',
    # 'src': 'external rooms api'}, {'name': 'Z.2.13a', 'roomcode': 'Z.2.13a', 'category_de': 'Büroarbeit', 'src': 'external rooms api'}]"""

    assert len(x.rooms) == 1

    # assert all(name in x.rooms[0].keys() for name in room_expected.keys())


def test_search_aau_api_organizations():
    x = AAICampusAPI().search('Abteilung für Server- und Kommunikationssysteme')
    assert len(x.organizations) == 1


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
