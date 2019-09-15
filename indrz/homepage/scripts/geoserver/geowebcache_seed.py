#!/bin/python
# -*- coding: utf-8 -*-
import os
import time
import logging
import requests
import json

from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')

logging.basicConfig(filename='/opt/roomlog.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('seed_geowebcache was called')

GEOSERVER_USERpass = GEOSERVER_USER + ":" + GEOSERVER_PASS

geoserver_url = "https://www.indrz.com/geoserver"

# reload_url = "http://localhost:8080/geoserver/rest/reload"
reload_url = geoserver_url + "/rest/reload"
layers_url = geoserver_url + "/rest/layers.json"
layer_groups = geoserver_url + "/rest/workspaces/indrz/layergroups.json"
seed_layers = geoserver_url + "/gwc/rest/seed.json"


def get_seed_status(s):
    """
    s = session object
    """
    # call_api = "curl -u " + GEOSERVER_USERpass + " -XPOST http://localhost:8080/geoserver/rest/reload"
    status_seed = s.get(url=seed_layers)
    return status_seed.json()


def get_layer_groups():
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    # call_api = "curl -u " + GEOSERVER_USERpass + " -XPOST http://localhost:8080/geoserver/rest/reload"
    reload_geoserver = s.get(url=layer_groups)
    print(reload_geoserver.status_code)
    resp = json.loads(reload_geoserver.text)
    layergroup_names = []
    print(resp)
    for k, v in resp.items():
        for x in v['layerGroup']:
            layergroup_names.append(x['name'])
            print(x['name'])
    return layergroup_names


def get_layers():
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    # call_api = "curl -u " + GEOSERVER_USERpass + " -XPOST http://localhost:8080/geoserver/rest/reload"
    reload_geoserver = s.get(url=layers_url)
    print(reload_geoserver.status_code)
    resp = json.loads(reload_geoserver.text)
    layernames = []
    for k, v in resp.items():
        print(v['layer'])
        for x in v['layer']:
            layernames.append(x['name'])
            print(x['name'])
    return layernames


def reload_geoserver():
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    # call_api = "curl -u " + GEOSERVER_USERpass + " -XPOST http://localhost:8080/geoserver/rest/reload"
    reload_geoserver = s.post(url=reload_url)
    print(reload_geoserver.status_code)
    print(reload_geoserver.text)


def seed_geowebcache():
    # This config file contains options for the gwc preseeding scripts
    # Zoom levels to create tiles for
    zoom_start = "14"
    zoom_stop = "22"
    number_threads = "14"  # threadCount=08  values 1 to 15 are recommended
    gwc_type = "reseed"  # type can be seed, reseed, truncate   all 3 are valid possibilities
    format_img = r"image/png"

    layers = ["indrz:ug01", "indrz:e00", "indrz:e01", "indrz:e02", "indrz:e03", "indrz:e04", "indrz:e05", "indrz:e06"]
    # layers = ["indrz:e06"]
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    # This script RESEED tiles meaning removes and creates in one go in the GWC cache

    for layer in layers:
        seed_url = geoserver_url + "/gwc/rest/seed/{0}.json".format(layer)

        data_update = json.dumps({"seedRequest": {
            "name": layer,
            # "bounds":{"coords":{ "double":["-124.0","22.0","66.0","72.0"]}},
            "srs": {"number": 3857},
            "zoomStart": 14,
            "zoomStop": 23,
            "format": format_img,
            "type": "reseed",
            "threadCount": number_threads
        }
        })

        seed_the_layer = s.post(url=seed_url, data=data_update)

        x = get_seed_status(s)
        while len(x['long-array-array']) > 0:
            x = get_seed_status(s)
            # print("in while! len > 0 len is: ", len(x['long-array-array']), " and layer is: ", layer)
            time.sleep(15)
        logging.info('done reseeding ' + layer)
        # time.sleep(40)  # wait 40 seconds before sending next layer to re-seed

# seed_geowebcache()

# call_api = "curl -u " + GEOSERVER_USERpass + " -XPOST http://localhost:8080/geoserver/rest/reload"
# http://gis.wu.ac.at:8080/geoserver/gwc/rest/seed/wuwien:og04
# Geoserver layers to perform Link with fix zoom level to all PC roomspreseeding operation on

# curlstring = "curl -u " + GEOSERVER_USERpass + " -XPOST -H 'Content-type: text/xml' -d \"<seedRequest><name>" + \
#              layer + "</name>" + \
#              "<srs><number>900913</number></srs>" + \
#              "<zoomStart>" + zoom_start + "</zoomStart>" + \
#              "<zoomStop>" + zoom_stop + "</zoomStop>" + \
#              "<format>" + format_img + "</format>" + \
#              "<type>" + gwc_type + "</type>" + \
#              "<threadCount>" + number_threads + "</threadCount>" + \
#              "</seedRequest>\" " + "\"" + geoserver_url + layer + ".xml" + '\"'
# print("\n processing layer " + layer + "\n curlstring call is: " + curlstring)
# os.system(curlstring)

# seed_geowebcache() # run the seed on all layers
# reload_geoserver()
# get_layers()
# get_layer_groups()
# seed_geowebcache()

# curl call to get status of reseed
# print "now status quick: " + str(os.system("curl -u " + GEOSERVER_USERpass + " -v -XGET " + "\"" + geoserver_url + layer + ".json" + '\"'))
# curl -u <user>:<password> -v -XGET http://localhost:8080/geoserver/gwc/rest/seed/wuwien:og06.json

# def addLayer2Geoserver(layer_name, workspaces, datastores):
#    cmd = "curl -u " + user_geoserver + ":" + pass_geoserver + " -XPOST -H 'Content-type: text/xml' -d '<featureType><name>" + layer_name
#    cmd = cmd + "</name></featureType>'   http://" + host_geoserver + "/geoserver"
#    cmd = cmd + "/rest/workspaces/" + workspaces + "/datastores/" + datastores + "/featuretypes"
#    return os.system(cmd)


# curl -v -u admin:geoserver -XPOST -H "Content-type: text/xml" -d '    # <seedRequest>
# <name>nurc:Arc_Sample</name>
# <srs><number>4326</number></srs>
# <zoomStart>1</zoomStart>
# <zoomStop>12</zoomStop>
# <format>image/png</format>
# <type>truncate</type>
# <threadCount>2</threadCount>
# </seedRequest>'
# "http://localhost:8080/geoserver/gwc/rest/seed/nurc:Arc_Sample.xml"


# This script removes tiles from the GWC cache
# for layer in layers:
#  curlstring="curl -u " + GEOSERVER_USERpass + " -XPOST -H 'Content-type: text/xml' -d '" + \
#             layer + "900913" + zoom_start + "" + zoom_stop + "image/pngtruncate2' " + geoserver_url + "/geoserver/gwc/rest/seed/" + layer + ".xml"
#  os.system(curlstring)
#  print "truncated " + layer

# This script is used to preseed gwc layers
# for layer in layers:
#  curlstring="curl -u " + GEOSERVER_USERpass + " -XPOST -H 'Content-type: text/xml' -d '" + layer + "900913" + zoom_start + "" + zoom_stop + "image/pngseed2' " + geoserver_url + "/geoserver/gwc/rest/seed/" + layer + ".xml"
#  os.system(curlstring)
#  print "seeded " + layer


# curl -v -u admin:geoserver -XPOST -H "Content-type: application/json" -d "{'seedRequest':{'name':'topp:states','bounds':{'coords':{ 'double':['-124.0','22.0','66.0','72.0']}},'srs':{'number':4326},'zoomStart':1,'zoomStop':12,'format':'image\/png','type':'truncate','threadCount':4}}}"  "http://localhost:8080/geoserver/gwc/rest/seed/nurc:Arc_Sample.json"
# curl -v -u admin:geoserver -XPOST -H "Content-type: text/xml" -d '<seedRequest><name>nurc:Arc_Sample</name><srs><number>4326</number></srs><zoomStart>1</zoomStart><zoomStop>12</zoomStop><format>image/png</format><type>truncate</type><threadCount>2</threadCount></seedRequest>'  "http://localhost:8080/geoserver/gwc/rest/seed/nurc:Arc_Sample.xml"

