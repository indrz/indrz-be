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
import time

import psycopg2
import requests
import json
import os

from dotenv import load_dotenv
load_dotenv(".env")

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')

# con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
# conn = psycopg2.connect(con_string)
# cur = conn.cursor()

from utils import unique_floor_names


#URL_BASE = "https://www.indrz.com/geoserver/rest"
URL_BASE = "https://tuw-maps.tuwien.ac.at/geoserver/rest"
headers_xml = {'Content-type': 'text/xml', }
headers_json = {'Content-type': 'application/json', }


def create_workspace(name):
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)
    data = '<workspace><name>' + name + '</name></workspace>'

    s.post(URL_BASE + '/rest/workspaces', headers=headers_xml, data=data)


def get_workspaces():
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)
    print(URL_BASE)
    r = s.get(URL_BASE + '/workspaces')

    print(r.status_code)

    print(r.text)
    res = json.loads(r.text)

    for space in res['workspaces']['workspace']:
        print(space['name'])

    print(type(res))

    print(r.text)




def create_featurestore(name):
    # /workspaces/{workspaceName}/datastores/{storeName}/featuretypes
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

   # myel =  		{"nativeCRS": "GEOGCS[\"WGS 84\", \n  DATUM[\"World Geodetic System 1984\", \n    SPHEROID[\"WGS 84\", 6378137.0, 298.257223563, AUTHORITY[\"EPSG\",\"7030\"]], \n    AUTHORITY[\"EPSG\",\"6326\"]], \n  PRIMEM[\"Greenwich\", 0.0, AUTHORITY[\"EPSG\",\"8901\"]], \n  UNIT[\"degree\", 0.017453292519943295], \n  AXIS[\"Geodetic longitude\", EAST], \n  AXIS[\"Geodetic latitude\", NORTH], \n  AUTHORITY[\"EPSG\",\"4326\"]]"}
   #
    crs = '''"PROJCS["WGS 84 / Pseudo-Mercator", 
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
  AUTHORITY["EPSG","3857"]]"'''

    d = {
	"featureType": {
		"name": name,
		"nativeName": name,
		"title": name,
		"abstract": name,
        "nativeCRS": {
            "_class": "projected",
            "__text": "PROJCS[\"WGS 84 / Pseudo-Mercator\",\n  GEOGCS[\"WGS 84\",\n    DATUM[\"World Geodetic System 1984\",\n      SPHEROID[\"WGS 84\", 6378137.0, 298.257223563, AUTHORITY[\"EPSG\",\"7030\"]],\n      AUTHORITY[\"EPSG\",\"6326\"]],\n    PRIMEM[\"Greenwich\", 0.0, AUTHORITY[\"EPSG\",\"8901\"]],\n    UNIT[\"degree\", 0.017453292519943295],\n    AXIS[\"Geodetic longitude\", EAST],\n    AXIS[\"Geodetic latitude\", NORTH],\n    AUTHORITY[\"EPSG\",\"4326\"]],\n  PROJECTION[\"Popular Visualisation Pseudo Mercator\", AUTHORITY[\"EPSG\",\"1024\"]],\n  PARAMETER[\"semi_minor\", 6378137.0],\n  PARAMETER[\"latitude_of_origin\", 0.0],\n  PARAMETER[\"central_meridian\", 0.0],\n  PARAMETER[\"scale_factor\", 1.0],\n  PARAMETER[\"false_easting\", 0.0],\n  PARAMETER[\"false_northing\", 0.0],\n  UNIT[\"m\", 1.0],\n  AXIS[\"Easting\", EAST],\n  AXIS[\"Northing\", NORTH],\n  AUTHORITY[\"EPSG\",\"3857\"]]"
        },
         "srs": "EPSG:3857",
		"nativeBoundingBox": {
			"minx": 1820700.70162944,
			"maxx": 1827407.17522951,
			"miny": 6136643.55439912,
			"maxy": 6141440.05205234,
			"crs": "EPSG:3857"
		},
		"latLonBoundingBox": {
			"minx": 16.3616244437537,
			"maxx": 16.413183012331135,
			"miny": 48.178746420817404,
			"maxy": 48.20148257557524,
			"crs": "EPSG:4326"
		},
		"projectionPolicy": "REPROJECT_TO_DECLARED",
		"enabled": True,
		"maxFeatures": 1000,
		"numDecimals": 6,
		"responseSRS": {
			"string": [
				4326
			]
		},
		"overridingServiceSRS": True,
		"skipNumberMatched": True,
		"circularArcPresent": True,
		"linearizationTolerance": 10,
		"attributes": {
			"attribute": [{
				"name": "geom",
				"minOccurs": 0,
				"maxOccurs": 1,
				"nillable": True,
				"binding": "org.locationtech.jts.geom.MultiPolygon"
			},
			{
				"name": "short_name",
				"minOccurs": 0,
				"maxOccurs": 1,
				"nillable": True
			},
			{
				"name": "room_code",
				"minOccurs": 0,
				"maxOccurs": 1,
				"nillable": True
			},
			{
				"name": "room_description",
				"minOccurs": 0,
				"maxOccurs": 1,
				"nillable": True
			},
			{
				"name": "space_type_id",
				"minOccurs": 0,
				"maxOccurs": 1,
				"nillable": True
			}]
		}
	}
}

    print(json.dumps(d))

    r = s.post(URL_BASE + '/workspaces/indrztu/datastores/ds-indrz-tu/featuretypes', headers=headers_json, data=json.dumps(d))
    # print(r.raise_for_status())
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)

    print(r.text)
    print(r.status_code)



def get_layers():
    """
    A layer is a published feature
    :return:
    """
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    r = s.get(URL_BASE + '/layers.json', headers=headers_xml)

    res = json.loads(r.text)
    print(r.text)
    if len(res['layers']) > 0:
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

def delete_layer(layer_name):

    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    headers = {'accept': 'application/json', 'content-type':'application/json'}
    del_url =  URL_BASE + "/workspaces/indrztu/datastores/ds-indrz-tu/featuretypes/" + layer_name
    print(del_url)
    r = s.delete(del_url, headers=headers)

    print(r.status_code, r.content, r.text)

    print("now deleting:, ", layer_name)

    # print(r.raise_for_status())
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)


def create_layer(new_feature_name, type, session):
    """

    :param new_feature_name:
    :param type: one of the following "spaces", "anno", "cartolines", "footprint"
    :return:
    """



    types = ['spaces', 'anno', 'cartolines', 'footprint', 'construction', 'wing', 'wing_points']

    if type not in types:
        print(f"sorry your type must equal one of the following {types}")
        return False

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
                        <name>indrztu:indrz-spaces</name>
                      </defaultStyle>

                    """

    native_srs = """
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

    bbox = """<nativeBoundingBox>
		<minx>1820700.70162944</minx>
		<maxx>1827407.17522951</maxx>
		<miny>6136643.55439912</miny>
		<maxy>6141440.05205234</maxy>
		<crs>EPSG:4326</crs>
	</nativeBoundingBox>
	<latLonBoundingBox>
		<minx>16.3616244437537</minx>
		<maxx>16.413183012331135</maxx>
		<miny>48.178746420817404</miny>
		<maxy>48.20148257557524</maxy>
		<crs>EPSG:4326</crs>
	</latLonBoundingBox>"""


    atts = ""
    if type == "spaces":
        atts = """	<attributes>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
             <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>room_code</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>short_name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>room_description</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>capacity</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>space_type_id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>floor_name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>floor_num</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""

    if type == "footprint":
        atts = """	<attributes>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
              <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>building_name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""

    if type == "anno":
        atts = """	<attributes>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
                         <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>room_code</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                            <attribute>
                <name>room_description</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                            <attribute>
                <name>space_type_id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""

    if type == "cartolines":
        atts = """	<attributes>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiLineString</binding>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>short_name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>

        </attributes>"""

    if type == "route":
        atts = """	<attributes>
                            <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
              <attribute>
                <name>network_type</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>cost</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""

    if type == "construction":
        atts = """	<attributes>
                            <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
              <attribute>
                <name>short_name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>organization</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""

    if type == "wing":
        atts = """	<attributes>
                            <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
              <attribute>
                <name>name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
                    <attribute>
                <name>abbreviation</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""

    if type == "wing_points":
        atts = """	<attributes>
            <attribute>
                <name>id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>geom</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <binding>org.locationtech.jts.geom.MultiPolygon</binding>
                <length>0</length>
            </attribute>
              <attribute>
                <name>name</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
          <attribute>
                <name>description</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
              <attribute>
                <name>category_id</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
        </attributes>"""


    data = "<featureType><name>" + new_feature_name + "</name>" + srs_3857 + bbox + "<srs>EPSG:3857</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy><enabled>true</enabled><advertised>false</advertised>"+  atts + "</featureType>"
    r = session.post(URL_BASE + '/workspaces/indrztu/datastores/ds-indrz-tu/featuretypes',
                      headers=headers_xml, data=data)
    # print(r.raise_for_status())
    print(r.content)
    print(r.reason)
    print(r.status_code)
    # print(r.text)


def assign_style_to_layer(floor_name, type, session):
    types = ['spaces', 'anno', 'cartolines', 'footprint', 'route', 'construction', 'wing', 'wing_points']

    if type not in types:
        print(f"sorry your type must equal one of the following {types}")
        return False
    style = ""

    if type == "spaces":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-spaces"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-spaces"
                    }
                ]
            }
        }}

    if type == "footprint":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-building-footprint"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-building-footprint"
                    }
                ]
            }
        }}

    if type == "cartolines":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-cartolines"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-cartolines"
                    }
                ]
            }
        }}

    if type == "anno":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-space-anno"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-space-anno"
                    }
                ]
            }
        }}

    if type == "route":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-routes"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-routes"
                    }
                ]
            }
        }}

    if type == "construction":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-construction"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-construction"
                    }
                ]
            }
        }}


    if type == "wing":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-wing"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-wing"
                    }
                ]
            }
        }}

    if type == "wing_points":
        style = {"layer": {
            "name": f"indrztu:{type}_{floor_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-wing-points"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrztu:indrz-wing-points"
                    }
                ]
            }
        }}

    # s = requests.Session()
    # s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    r = session.put(URL_BASE + f"/workspaces/indrztu/layers/{type}_{floor_name}", headers=headers_json,
                     data=json.dumps(style))
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
                        <published type="layer"><name>indrz:{0}_construction</name></published>
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
    r = s.post(URL_BASE + "workspaces/indrz/layergroups", headers=headers_xml, data=post_data)
    # r = s.get(url_base + "workspaces/indrz/layergroups", geoserver_auth=geoserver_auth, headers=headers)
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)

def generate_groups(floor_name, session):

    group_names = ['footprint', 'spaces', 'cartolines', 'anno', 'construction', 'wing_points']

    post_data = """<?xml version="1.0" encoding="UTF-8"?>
                    <layerGroup>
                      <name>floor_{0}</name>
                      <title>floor_{0}</title>
                        <workspace>
                            <name>indrztu</name>
                        </workspace>
                      <publishables>
                        <published type="layer"><name>indrztu:footprint_{0}</name></published>
                        <published type="layer"><name>indrztu:spaces_{0}</name></published>
                        <published type="layer"><name>indrztu:cartolines_{0}</name></published>
                        <published type="layer"><name>indrztu:anno_{0}</name></published>
                        <published type="layer"><name>indrztu:wing_points_{0}</name></published>
                        <published type="layer"><name>indrztu:construction_{0}</name></published>
                      </publishables>
                       <bounds>
                        <minx>1820700.70162944</minx>
                        <maxx>1827407.17522951</maxx>
                        <miny>6136643.55439912</miny>
                        <maxy>6141440.05205234</maxy>
                        <crs class="projected">EPSG:3857</crs>
                      </bounds>
                      <attribution>
                        <logoWidth>0</logoWidth>
                        <logoHeight>0</logoHeight>
                      </attribution>

                    </layerGroup>""".format(floor_name)

    print(post_data)

    b = {"layerGroup": {
        "name": f"indrztu:floor_{floor_name}",
        "mode": "SINGLE",
        "title": f"{floor_name}",
        "abstractTxt": "string",
        "workspace": {
            "name": "indrztu"
        },
        "publishables": {
            "published": [
                {"type": "layer", "name": f"indrztu:footprint_{floor_name}"},
                {"type": "layer", "name": f"indrztu:spaces_{floor_name}"},
                {"type": "layer",  "name": f"indrztu:cartolines_{floor_name}"},
                {"type": "layer", "name": f"indrztu:anno_{floor_name}",},
                {"type": "layer", "name": f"indrztu:wing_points_{floor_name}", },
                {"type": "layer", "name": f"indrztu:construction_{floor_name}", }
            ]
        },
        "bounds": {
            "minx": 1820700.70162944,
            "maxx": 1827407.17522951,
            "miny": 6136643.55439912,
            "maxy": 6141440.05205234,
            "crs": "EPSG:3857"
        }
    }
    }

    r = session.post(URL_BASE + "/layergroups", headers=headers_xml, data=post_data)

    # r = s.post(URL_BASE + "/layergroups", headers=headers_json, data=json.dumps(b))

    print(f"creating group called floor_{floor_name} ")
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

def create_style(name, filename, session):

    data = {
        "style": {
            "name": "indrz_spaces",
            "filename": "indrz_spaces.sld"
        }
    }
    headers = {'content-type': 'application/vnd.ogc.sld+xml'}
    style_url = URL_BASE + "/styles"
    xmlfile = open('trb-1996-219.xml', 'rb')

    session.post(style_url, data=data, files=xmlfile, headers=headers)


def run_assign_stlye():
    """DOES NOT WORK"""
    for floor in levels_abrev:
        assign_style_to_layer(floor, "space_polys", 'indrz:indrz-spaces')


# run_assign_stlye()

def run_create_layers():
    for floor in levels_abrev:
        for layer in layers:
            create_layer("{0}{1}".format(floor, layer))


if __name__ == '__main__':

    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    # GENERATE LAYERS
    # types = ['footprint', 'spaces', 'cartolines', 'anno', 'construction' ]
    # types = ["cartolines", "anno", "routes"]

    # uncomment this to create geoserver layer with style
    # you must first create the sld style manually in geoserver
    # before you run this

    # types = ['wing', 'wing_points']
    #

    # get_workspaces()
    # get_layers()

    # types = ['spaces', ]
    # for type in types:
    #     for floor_name in unique_floor_names:
    #         create_layer(f'{type}_{floor_name.lower()}', type, session=s)
    #         time.sleep(4)
    #         print(f"now running floor {type} - {floor_name.lower()}")
    #         assign_style_to_layer(floor_name.lower(), type, session=s)

    # generate GROUPS
    for floor_name in unique_floor_names:
        time.sleep(3)
        generate_groups(floor_name.lower(), session=s)

    # assign_style_to_layer(floor_name.lower(), 'anno')
    #delete_layer('route_01')
    # curl -X DELETE http://localhost:8080/geoserver/rest/workspaces/abc/datastores/gtu/featuretypes/tom -H  "accept: application/json" -H  "content-type: application/json"
    # delete_layer('spaces')

    s.close()




