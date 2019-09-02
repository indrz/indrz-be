from urllib import parse

import pytest
from django.test import Client, TestCase, RequestFactory, SimpleTestCase
from django.conf import settings

from settings.secret_settings import aau_client_secret, aau_client_id
# from django.test import SimpleTestCase
from homepage.aau_campus_api import AAICampusAPI
from settings import secret_settings

import requests, json
import pprint

settings.configure()


s = requests.Session()

auth_url = "https://campus-api.aau.at/oauth/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(aau_client_id, aau_client_secret)
auth_resp = s.get(auth_url)

print(auth_resp.content)

access_token = auth_resp.json()['access_token']

search_term = "Fabian Rainer"

person = s.get('https://campus-api.aau.at/v1/cgis/search/staff?name={1}&access_token={0}'.format(access_token, search_term))
org = s.get('https://campus-api.aau.at/v1/cgis/search/ou?name={1}&access_token={0}'.format(access_token, search_term))
resp_all_rooms = s.get('https://campus-api.aau.at/v1/cgis/search/rooms?&access_token={0}'.format(access_token))

print(person.json())

all_rooms = resp_all_rooms.json()
one_room = {'buildingname': 'Hauptgebäude, Zentraltrakt', 'buildingcolor': None, 'capacity': None, 'category_de': 'Betriebs-technische Anlagen', 'category_en': None, 'fancyname_de': None, 'fancyname_en': None, 'floorname': 'Ebene 1', 'pk_big': None, 'roomcode': 'Z.1.10b', 'roomname_de': 'Projektionsraum', 'roomname_en': None, 'tid': 682}
print(all_rooms[0])
print(len(all_rooms))



response_shouldbe = {'token_type': 'bearer', 'expires_in': 43133, 'access_token': 'edc7ccfb-9c12-434c-b77a-3429d882fc26', 'scope': 'cgis'}

aau_org_api_keys = ["name", "bezeichnung", "raum_key", "raum_code", "foobar"]
aau_staff_api_keys = ["firstname", "room_keys", "orgkeys", "lastname", "rooms"]