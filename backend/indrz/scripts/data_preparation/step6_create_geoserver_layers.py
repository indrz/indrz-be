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
import os
import requests
import json

from utils import unique_floor_map
GEOSERVER_PASS = 'air'
GEOSERVER_USER = 'indrzadmin'

# URL_BASE = "https://www.indrz.com/geoserver/rest"
# URL_BASE = "http://localhost:8600/geoserver/rest"

# the URL_BASE here works when running from inside indrz-boku-api:3.0 container
# URL_BASE = "http://geoserver:8080/geoserver/rest"
#URL_BASE = "http://localhost:8080/geoserver/rest"

URL_BASE = "http://geoserveraau:8080/geoserver/rest"
headers_xml = {'Content-type': 'text/xml', }
headers_json = {'Content-type': 'application/json', }
supported_types = ['spaces', 'anno', 'cartolines', 'footprint', 'route',
                   'construction', 'wing', 'wing_points', 'campuses', 'buildings', 'entrances']




minx_3857 = 1586817.05
miny_3857 = 5877911.95
maxx_3857 = 1595403.12
maxy_3857 = 5882977.62

minx_4326 = 15.764322
miny_4326 = 47.7213553
maxx_4326 = 16.712229
maxy_4326 = 48.4788779

import requests


def create_geoserver_workspace(base_url, workspace_name, username, password):
    """
    Create a new GeoServer workspace via the REST API.

    Args:
        base_url (str): The base URL of the GeoServer instance (e.g., 'http://localhost:8080/geoserver').
        workspace_name (str): The name of the new workspace to create.
        username (str): The username to authenticate with GeoServer.
        password (str): The password to authenticate with GeoServer.

    Returns:
        True if the workspace was created successfully, False otherwise.
    """

    # Set the URL for creating a new workspace
    url = f"{base_url}/rest/workspaces"

    # Set the headers for the request
    headers = {
        "Content-type": "application/xml",
        "Accept": "application/xml"
    }

    # Set the XML payload for the request
    payload = f"""
        <workspace>
            <name>{workspace_name}</name>
        </workspace>
    """

    # Make the POST request to create the workspace
    response = requests.post(url, headers=headers, data=payload, auth=(username, password))

    # Check if the workspace was created successfully
    if response.status_code == 201:
        return True
    else:
        return False


def create_geoserver_datastore(base_url, workspace_name, datastore_name, db_host, db_port,
                               db_name, db_user, db_password, username, password):
    """
    Create a new GeoServer workspace and datastore via the REST API.

    Args:
        base_url (str): The base URL of the GeoServer instance (e.g., 'http://localhost:8080/geoserver').
        workspace_name (str): The name of the new workspace to create.
        datastore_name (str): The name of the new datastore to create.
        db_host (str): The hostname of the PostGIS database server.
        db_name (str): The name of the PostGIS database.
        db_user (str): The username to connect to the PostGIS database.
        db_password (str): The password to connect to the PostGIS database.
        username (str): The username to authenticate with GeoServer.
        password (str): The password to authenticate with GeoServer.

    Returns:
        True if the workspace and datastore were created successfully, False otherwise.
    """

    # Set the headers
    headers = {
        "Content-type": "application/xml",
        "Accept": "application/xml"
    }


    # Set the URL for creating a new datastore
    datastore_url = f"{base_url}/rest/workspaces/{workspace_name}/datastores"



    # Set the XML payload for the datastore request
    datastore_payload = f"""
        <dataStore>
            <name>{datastore_name}</name>
            <connectionParameters>
                <host>{db_host}</host>
                <port>{db_port}</port>
                <database>{db_name}</database>
                <user>{db_user}</user>
                <passwd>{db_password}</passwd>
                <dbtype>postgis</dbtype>
                <schema>geodata</schema>
                <namespace>{workspace_name}</namespace>
            </connectionParameters>
        </dataStore>
    """

    # Make the POST request to create the datastore
    datastore_response = requests.post(datastore_url, headers=headers, data=datastore_payload, auth=(username, password))

    # Check if the datastore was created successfully
    if datastore_response.status_code == 201:
        return True
    else:
        print(f"error {datastore_response.text}")
        return False


def create_geoserver_layer(base_url, workspace_name, datastore_name, layer_name, username, password):
    """
    Create a new GeoServer layer via the REST API.

    Args:
        base_url (str): The base URL of the GeoServer instance (e.g., 'http://localhost:8080/geoserver').
        workspace_name (str): The name of the workspace that contains the datastore.
        datastore_name (str): The name of the datastore that contains the data.
        layer_name (str): The name to give the new layer.
        username (str): The username to authenticate with GeoServer.
        password (str): The password to authenticate with GeoServer.

    Returns:
        True if the layer was created successfully, False otherwise.
    """

    # Set the URL for creating a new layer
    layer_url = f"{base_url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes"

    # Set the headers for the layer request
    headers = {
        "Content-type": "application/xml",
        "Accept": "application/xml"
    }

    # Set the XML payload for the layer request
    layer_payload = f"""
        <featureType>
            <name>{layer_name}</name>
        </featureType>
    """

    # Make the POST request to create the layer
    layer_response = requests.post(layer_url, headers=headers, data=layer_payload, auth=(username, password))

    # Check if the layer was created successfully
    if layer_response.status_code == 201:
        print(f"created layer {layer_name}")
        return True
    else:
        print(f"error {layer_response.text}")
        return False


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
                "minx": {minx_3857},
                "maxx": {maxx_3857},
                "miny": {miny_3857},
                "maxy": {maxy_3857},
                "crs": "EPSG:3857"
            },
            "latLonBoundingBox": {
                "minx": {minx_4326},
                "maxx": {maxx_4326},
                "miny": {miny_4326},
                "maxy": {maxy_4326},
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

    r = s.post(URL_BASE + '/workspaces/indrz/datastores/indrz/featuretypes', headers=headers_json, data=json.dumps(d))
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

    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    del_url = URL_BASE + "/workspaces/indrz/datastores/indrz/featuretypes/" + layer_name
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

    if type not in supported_types:
        print(f"sorry your type must equal one of the following {type}")
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
                        <name>indrz:indrz-spaces</name>
                      </defaultStyle>

                    """

    bbox = f"""<nativeBoundingBox>
		<minx>{minx_3857}</minx>
		<maxx>{maxx_3857}</maxx>
		<miny>{miny_3857}</miny>
		<maxy>{maxy_3857}</maxy>
		<crs>EPSG:4326</crs>
	</nativeBoundingBox>
	<latLonBoundingBox>
		<minx>{minx_4326}</minx>
		<maxx>{maxx_4326}</maxx>
		<miny>{miny_4326}</miny>
		<maxy>{maxy_4326}</maxy>
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
                <name>name</name>
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
                <name>building_name</name>
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

    if type == "campuses":
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
        </attributes>
        """

    if type == "buildings":
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
                <binding>org.locationtech.jts.geom.Point</binding>
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
                <name>building_name</name>
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
                <name>street</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>house_number</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>                    
            <attribute>
                <name>postal_code</name>
                <minOccurs>0</minOccurs>
                <maxOccurs>1</maxOccurs>
                <nillable>true</nillable>
                <length>0</length>
            </attribute>
            <attribute>
                <name>city</name>
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
                <name>long_name</name>
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

    if type == "entrances":
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
                <name>floor_num</name>
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

    store = f"""	<store>
		<@class>dataStore</@class>
		<name>indrz:indrz</name>
		<href>http://localhost:8080/geoserver/rest/workspaces/indrz/datastores/indrz.json</href>
	</store>"""

    xml = f"""    <FeatureTypeInfo>
        <name>{new_feature_name}</name>
        <nativeName>{new_feature_name}</nativeName>
        <namespace>
            <name>indrz</name>
        </namespace>
        <title>{type}</title>
        <metadatalinks>
            <metadataLink>
                <type>string</type>
                <metadataType>string</metadataType>
                <content>string</content>
            </metadataLink>
        </metadatalinks>
        <dataLinks>
            <metadataLink>
                <type>string</type>
                <content>string</content>
            </metadataLink>
        </dataLinks>
        {srs_3857}
        <srs>EPSG:4326</srs>
        {bbox}
        <cqlFilter>INCLUDE</cqlFilter>
        <responseSRS>
            <string>
                <0>4326</0>
            </string>
        </responseSRS>
        {atts}
    </FeatureTypeInfo>"""

    data = "<featureType><name>" + new_feature_name + "</name>" + srs_3857 + bbox + "<srs>EPSG:3857</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy><enabled>true</enabled><advertised>false</advertised>" + atts + "</featureType>"
    # print(data)
    # print(xml)
    r = session.post(URL_BASE + '/workspaces/indrz/datastores/indrz/featuretypes',
                     headers=headers_xml, data=data)
    # print(r.raise_for_status())
    # print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)

def ai_assign_style(layer_name, style_name, workspace):
    from requests.auth import HTTPBasicAuth

    # Set GeoServer details
    geoserver_url = "http://localhost:8080/geoserver/rest/"


    # # Set layer and style details
    # workspace = "myWorkspace"
    # layer_name = "myLayer"
    # style_name = "indrz-spaces"

    # Make the PUT request
    headers = {"Content-type": "text/xml"}
    data = "<layer><defaultStyle><name>{}</name></defaultStyle></layer>".format(style_name)
    layer_url = f"{base_url}/rest/workspaces/{workspace}/layers/{layer_name}"
    response = requests.put(layer_url, auth=HTTPBasicAuth(GEOSERVER_USER, GEOSERVER_PASS), headers=headers, data=data)

    # Check the response
    if response.status_code == 200:
        print("Style successfully set!")
    else:
        print("Failed to set style. Response code:", response.status_code)

def assign_style_to_layer(geoserver_lyr_name, type, session):
    geoserver_lyr_name = str(geoserver_lyr_name)
    if type not in supported_types:
        print(f"sorry your type must equal one of the following {type}")
        return False
    style = ""

    if type == "spaces":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-spaces"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-spaces"
                    }
                ]
            }
        }}

    if type == "footprint":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-building-footprint"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-building-footprint"
                    }
                ]
            }
        }}

    if type == "buildings":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-buildings"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-buildings"
                    }
                ]
            }
        }}

    if type == "cartolines":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-cartolines"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-cartolines"
                    }
                ]
            }
        }}

    if type == "anno":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-space-anno"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-space-anno"
                    }
                ]
            }
        }}

    if type == "route":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-routes"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-routes"
                    }
                ]
            }
        }}

    if type == "construction":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-construction"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-construction"
                    }
                ]
            }
        }}
    if type == "campuses":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-campuses"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-campuses"
                    }
                ]
            }
        }}

    if type == "wing":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-wing"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-wing"
                    }
                ]
            }
        }}

    if type == "wing_points":
        style = {"layer": {
            "name": f"indrz:{geoserver_lyr_name}",
            "path": "string",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "indrz-wing-points"
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "indrz:indrz-wing-points"
                    }
                ]
            }
        }}

    # s = requests.Session()
    # s.auth = (GEOSERVER_USER, GEOSERVER_PASS)
    print(style)
    # print(json.dumps(style))

    style_url = URL_BASE + f"/workspaces/indrz/layers/{geoserver_lyr_name}"
    print(style_url)

    r = session.put(style_url, headers=headers_json, data=json.dumps(style))
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
    post_data = f"""<?xml version="1.0" encoding="UTF-8"?>
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
    # group_names = ['footprint', 'spaces', 'cartolines', 'anno', 'construction', 'wing_points']


    post_data = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <layerGroup>
                      <name>floor_{floor_name}</name>
                      <title>floor_{floor_name}</title>
                        <workspace>
                            <name>indrz</name>
                        </workspace>
                      <publishables>
                        <published type="layer"><name>indrz:buildings</name></published>
                        <published type="layer"><name>indrz:campuses</name></published>
                        <published type="layer"><name>indrz:footprint_{floor_name}</name></published>
                        <published type="layer"><name>indrz:spaces_{floor_name}</name></published>
                        <published type="layer"><name>indrz:cartolines_{floor_name}</name></published>
                        <published type="layer"><name>indrz:anno_{floor_name}</name></published>
                      </publishables>
                       <bounds>
                        <minx>{minx_3857}</minx>
                        <maxx>{maxx_3857}</maxx>
                        <miny>{miny_3857}</miny>
                        <maxy>{maxy_3857}</maxy>
                        <crs class="projected">EPSG:3857</crs>
                      </bounds>
                      <attribution>
                        <logoWidth>0</logoWidth>
                        <logoHeight>0</logoHeight>
                      </attribution>

                    </layerGroup>"""

    b = {"layerGroup": {
        "name": f"indrz:floor_{floor_name}",
        "mode": "SINGLE",
        "title": f"{floor_name}",
        "abstractTxt": "string",
        "workspace": {
            "name": "indrz"
        },
        "publishables": {
            "published": [
                # {"type": "layer", "name": f"indrz:footprint_{floor_name}"},
                {"type": "layer", "name": f"indrz:spaces_{floor_name}"},
                {"type": "layer", "name": f"indrz:cartolines_{floor_name}"},
                {"type": "layer", "name": f"indrz:anno_{floor_name}", }

            ]
        },
        "bounds": {
            "minx": minx_3857,
            "maxx": maxx_3857,
            "miny": miny_3857,
            "maxy": maxy_3857,
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


def create_layer_group(workspace, group_name, layer_names):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Create the layer group
    group_url = f'{URL_BASE}/{workspace}/layergroups'
    group_data = {
        "layerGroup": {
            "name": group_name,
            "mode": "SINGLE",
            "title": group_name,
            "publishables": {
                "published": [{"type": "layer", "name": f"{workspace}:{layer_name}"} for layer_name in layer_names]
            }
        }
    }

    response = requests.post(
        group_url,
        headers=headers,
        data=json.dumps(group_data),
        auth=(GEOSERVER_USER, GEOSERVER_PASS),
    )

    if response.status_code != 201:
        print(f'Failed to create layer group: {response.text}')
        return

    print(f'Layer group {group_name} created with layers {", ".join(layer_names)}')

# Example usage:
# create_layer_group('indrz', 'your_layer_group', ['layer1', 'layer2', 'layer3'])



def create_style(name, filename, session):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    headers = {'content-type': 'application/vnd.ogc.sld+xml'}
    style_url = URL_BASE + "/workspaces/indrz/styles"
    filepath = os.path.join(BASE_DIR, "geoserver", f"{filename}.sld")
    print(filepath)
    with open(filepath, 'rb') as xmlfile:
        resp = session.post(style_url, data=xmlfile, headers=headers)
        print("created sld ", resp.status_code, resp.text)


def run_assign_stlye():
    """DOES NOT WORK"""
    for floor in levels_abrev:
        assign_style_to_layer(floor, "space_polys", 'indrz:indrz-spaces')


# run_assign_stlye()

def run_create_layers():
    for floor in levels_abrev:
        for layer in layers:
            create_layer("{0}{1}".format(floor, layer))


def create_all_layers(types, s):
    for type in types:
        for floor in unique_floor_map:
            floor_float = floor['number']
            new_layer_name = f'{type}_{floor_float}'
            geos_layername = new_layer_name.replace('-', 'u').replace('.', '_')

            print(geos_layername)
            # create_layer(geos_layername, type, session=s)
            create_geoserver_layer(base_url, workspace_name, datastore_name, geos_layername, GEOSERVER_USER,
                                   GEOSERVER_PASS)
            # time.sleep(4)
            print(f"now running floor {geos_layername}")
            assign_style_to_layer(geos_layername, type, session=s)


def create_all_groups():

    for floor in unique_floor_map:
        floor_float = floor['number']
        new_layer_name = str(floor_float)
        geoserver_groupname = new_layer_name.replace('-', 'u').replace('.', '_')
        time.sleep(3)
        generate_groups(geoserver_groupname, session=s)
        # create_layer_group(workspace='indrz', group_name=geoserver_groupname, layer_names=lyr_names)


def get_featuretypes(s):
    r = s.get(URL_BASE + "/workspaces/indrz/datastores/indrz/featuretypes")
    print(r.status_code)
    print("new")
    print(r.text)


def create_campuses_layer(geos_layername, s):
    create_layer(geos_layername, type='campuses', session=s)
    time.sleep(4)
    # print(f"now running floor {geos_layername}")
    # assign_style_to_layer(geos_layername, type='campuses', session=s)


def create_buildings_layer(geos_layername, s):
    create_layer(geos_layername, type='buildings', session=s)
    time.sleep(4)
    print(f"now running floor {geos_layername}")
    assign_style_to_layer(geos_layername, type='buildings', session=s)


if __name__ == '__main__':
    s = requests.Session()
    s.auth = (GEOSERVER_USER, GEOSERVER_PASS)

    # Step 1. Create workspace
    base_url = "http://geoserveraau:8080/geoserver"
    workspace_name = "indrz"
    datastore_name = "indrz"
    pg_username = "indrzaau"
    pg_password = "air"

    # step 1 create workspace
    # result = create_geoserver_workspace(base_url, workspace_name, GEOSERVER_USER, GEOSERVER_PASS)
    #
    # if result:
    #     print(f"Workspace {workspace_name} created successfully!")
    # else:
    #     print("Error creating workspace.")

    # Step 2. create datastore ie db connection
    # ds_result = create_geoserver_datastore(base_url, workspace_name='indrz', datastore_name='indrz',
    #                                        db_password=pg_password, db_host='indrz_db', db_port='5432',
    #                                        db_name=pg_username, db_user='indrzaau',
    #                                        username=GEOSERVER_USER, password=GEOSERVER_PASS)
    #
    # if ds_result:
    #     print(f"Datastore {datastore_name} created successfully!")
    # else:
    #     print("Error creating workspace.")
    #
    #
    #
    # layer_name = "my_new_layer"
    #
    # create_geoserver_layer(base_url, workspace_name, datastore_name, "spaces_0_0", GEOSERVER_USER, GEOSERVER_PASS)

    # get_workspaces()
    # get_layers()

    # STEP 3 create sld styles and upload to geoserver
    # sld_styles = ['indrz-building-footprint', 'indrz-cartolines', 'indrz-construction', 'indrz-outdoor-poi',
    #                 'indrz-space-anno', 'indrz-spaces', 'indrz-wing-points', 'indrz-wing', 'indrz-campuses']
    # for sld_name in sld_styles:
    #     create_style(name=sld_name, filename=sld_name, session=s)

    # Step 4. GENERATE LAYERS
    # Step 4. GENERATE LAYERS
    # types = ['footprint', 'cartolines', 'spaces', 'anno', 'wing', 'wing_points', 'campuses', 'buildings']
    #
    # create_geoserver_layer(base_url, "indrz", "indrz", "campuses", GEOSERVER_USER, GEOSERVER_PASS)
    # ai_assign_style("buildings","indrz-buildings", "indrz")
    #
    # create_geoserver_layer(base_url, "indrz", "indrz", "buildings", GEOSERVER_USER, GEOSERVER_PASS)
    # ai_assign_style("buildings","indrz-buildings", "indrz")

    # types = ['campuses', 'buildings']
    # create_all_layers(types, s)

    # Step 5. generate GROUPS
    create_all_groups()

    # assign_style_to_layer(floor_name.lower(), 'anno')
    # delete_layer('route_01')
    # curl -X DELETE http://localhost:8080/geoserver/rest/workspaces/abc/datastores/gtu/featuretypes/tom -H  "accept: application/json" -H  "content-type: application/json"
    # delete_layer('spaces')

    s.close()
