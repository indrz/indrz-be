# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with th
# is program.  If not, see <http://www.gnu.org/licenses/>.
import psycopg2
import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')

# con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
# conn = psycopg2.connect(con_string)
# cur = conn.cursor()



URL_BASE = "https://www.indrz.com/geoserver/rest"
headers = {'Content-type': 'text/xml', }


def create_workspace(name):
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)
    data = '<workspace><name>' + name + '</name></workspace>'

    s.post(URL_BASE + '/rest/workspaces', headers=headers, data=data)


def get_workspaces():
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)
    print(URL_BASE)
    r = s.get(URL_BASE + '/workspaces')

    res = json.loads(r.text)

    for space in res['workspaces']['workspace']:
        print(space['name'])

    print(type(res))

    print(r.text)


get_workspaces()


def get_layers():
    """
    A layer is a published feature
    :return:
    """
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    r = s.get(URL_BASE + '/rest/layers.json', headers=headers)

    res = json.loads(r.text)
    print(r.text)
    for lyr in res['layers']['layer']:
        print(lyr)
    print(type(res))

    print(r.text)


def get_imports():
    """
    A layer is a published feature
    :return:
    """
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    r = s.get(URL_BASE + '/rest/imports', headers=headers)

    print(r.text)


def update_geoserver_layer(layer_name):
    pass

# PUT / geoserver / rest / workspaces / < workspace > / datastores / < data_store > / featuretypes / < layer_name >
#
#     < featureType >
#     < enabled > true < / enabled >
#     < advertised > false < / advertised >
#
# < / featureType >


def create_layer(new_feature_name):
    # curl - v - u
    # admin:geoserver - XPOST - H
    # "Content-type: text/xml"
    # -drver / rest / workspaces / acme / datastores / nyc / featuretypes
    # "<featureType><name>buildings</name></featureType>"
    # http: // localhost:8080 / geose
    """

    :param new_feature_name:
    :return:
    """
    srs_3857 = """
    <nativeCRS class="projected">PROJCS["WGS 84 / Pseudo-Mercator", 
  GEOGCS["WGS 84", 
    DATUM["World Geodetic System 1984", 
      SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]], 
      AUTHORITY["EPSG","6326"]], 
    PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], 
    UNIT["degree", 0.017453292519943295], 
    AXIS["Geodetic longitude", EAST], 
    AXIS["Geodetic latitude", NORTH], 
    AUTHORITY["EPSG","4326"]], 
  PROJECTION["Popular Visualisation Pseudo Mercator", AUTHORITY["EPSG","1024"]], 
  PARAMETER["semi_minor", 6378137.0], 
  PARAMETER["latitude_of_origin", 0.0], 
  PARAMETER["central_meridian", 0.0], 
  PARAMETER["scale_factor", 1.0], 
  PARAMETER["false_easting", 0.0], 
  PARAMETER["false_northing", 0.0], 
  UNIT["m", 1.0], 
  AXIS["Easting", EAST], 
  AXIS["Northing", NORTH], 
  AUTHORITY["EPSG","3857"]]</nativeCRS>
  """

    layer_style = """
                      <defaultStyle>
                        <name>indrz:indrz-spaces</name>
                      </defaultStyle>
                
                    """

    native_srs = """
      <nativeCRS class="projected">PROJCS[&quot;WGS 84 / Pseudo-Mercator&quot;,
      GEOGCS[&quot;WGS 84&quot;,
        DATUM[&quot;World Geodetic System 1984&quot;,
          SPHEROID[&quot;WGS 84&quot;, 6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],
          AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],
        PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],
        UNIT[&quot;degree&quot;, 0.017453292519943295],
        AXIS[&quot;Geodetic longitude&quot;, EAST],
        AXIS[&quot;Geodetic latitude&quot;, NORTH],
        AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]],
      PROJECTION[&quot;Popular Visualisation Pseudo Mercator&quot;, AUTHORITY[&quot;EPSG&quot;,&quot;1024&quot;]],
      PARAMETER[&quot;semi_minor&quot;, 6378137.0],
      PARAMETER[&quot;latitude_of_origin&quot;, 0.0],
      PARAMETER[&quot;central_meridian&quot;, 0.0],
      PARAMETER[&quot;scale_factor&quot;, 1.0],
      PARAMETER[&quot;false_easting&quot;, 0.0],
      PARAMETER[&quot;false_northing&quot;, 0.0],
      UNIT[&quot;m&quot;, 1.0],
      AXIS[&quot;Easting&quot;, EAST],
      AXIS[&quot;Northing&quot;, NORTH],
      AUTHORITY[&quot;EPSG&quot;,&quot;3857&quot;]]</nativeCRS>

    """

    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    data = "<featureType><name>" + new_feature_name + "</name>" + srs_3857 + "<srs>EPSG:3857</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy><enabled>true</enabled><advertised>false</advertised></featureType>"
    r = s.post(URL_BASE + 'workspaces/indrz/datastores/indrz-aau/featuretypes',
                      headers=headers, data=data)
    # print(r.raise_for_status())
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)


def assign_style_to_layer(floor, layer, sld_name):
    """DOES NOT WORK AT ALL"""
    style_data = """<?xml version="1.0" encoding="UTF-8"?>
                    <layer>
                        <name>indrz:{0}{1}</name>
                    
                        <defaultStyle>
                            <name>indrz:{2}</name>
                        </defaultStyle>
                    
                    </layer>""".format(floor, layer, sld_name)

    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    r = s.put(URL_BASE + 'layers/{0}{1}'.format(floor, layer), headers=headers,
                     data=style_data)
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)
    # print(r.raise_for_status())


# levels_abrev = ('e01_', 'e02_', 'e03_')
# grp_names= ("e01", "e02", "e03")
# layers = ('carto_lines', 'floor_footprint', 'space_polys')
# sld_styles = ("indrz-spaces", "indrz-cartolines", "indrz-building-footprint", "space-anno")


def create_groups(grp_name):
    """ This works CHANGE BOUNDS !!! """
    post_data = """<?xml version="1.0" encoding="UTF-8"?>
                    <layerGroup>
                      <name>{0}</name>
                      <title>{0}</title>
                      <publishables>
                        <published type="layer"><name>indrz:{0}_floor_footprint</name></published>
                        <published type="layer"><name>indrz:{0}_space_polys</name></published>
                        <published type="layer"><name>indrz:{0}_carto_lines</name></published>
                        <published type="layer"><name>indrz:{0}_space_anno</name></published>
                      </publishables>
                       <bounds>
                        <minx>1587621.59469851</minx>
                        <maxx>1588569.86802779</maxx>
                        <miny>5879205.19569104</miny>
                        <maxy>5880025.69724888</maxy>
                        <crs class="projected">EPSG:3857</crs>
                      </bounds>
                      <attribution>
                        <logoWidth>0</logoWidth>
                        <logoHeight>0</logoHeight>
                      </attribution>

                    </layerGroup>""".format(grp_name)


    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)


    print(URL_BASE + "workspaces/indrz/layergroups")
    r = s.post(URL_BASE + "workspaces/indrz/layergroups", headers=headers, data=post_data)
    # r = s.get(url_base + "workspaces/indrz/layergroups", geoserver_auth=geoserver_auth, headers=headers)
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)


# def run_create_groups():
#
#     for grp in grp_names:
#         create_groups(grp)
#
# run_create_groups()

def create_style(name, filename):
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    data = {
        "style": {
            "name": "indrz_spaces",
            "filename": "indrz_spaces.sld"
        }
    }
    headers = {'content-type': 'application/vnd.ogc.sld+xml'}
    style_url = URL_BASE + "/styles"
    xmlfile = open('trb-1996-219.xml', 'rb')

    s.post(style_url, data=data, files=xmlfile, headers=headers)


def run_assign_stlye():
    """DOES NOT WORK"""
    for floor in levels_abrev:
        assign_style_to_layer(floor, "space_polys", 'indrz:indrz-spaces')


# run_assign_stlye()

def run_create_layers():
    for floor in levels_abrev:
        for layer in layers:
            create_layer("{0}{1}".format(floor, layer))

# get_workspaces()
# get_layers()
#
# get_imports()

# for level in levels_abrev:
#     opt = '<nativeName>{0}space_polys</nativeName>'.format(level)
#     curlevel = '{0}space_anno'.format(level)
#     print(curlevel, opt)
#
#     create_layer(curlevel)
