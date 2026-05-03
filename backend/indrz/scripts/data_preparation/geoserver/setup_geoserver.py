import requests
import json

# Replace these variables with your GeoServer credentials and URL
GEOSERVER_USER = 'your_geoserver_username'
GEOSERVER_PASSWORD = 'your_geoserver_password'
GEOSERVER_URL = 'http://your_geoserver_url:8080/geoserver'

def create_layer(workspace, datastore, layer_name, style_name, srs, bbox_native, bbox_latlong):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Create the layer
    layer_url = f'{GEOSERVER_URL}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes'
    layer_data = {
        'featureType': {
            'name': layer_name,
            'nativeName': layer_name,
            'title': layer_name,
            'enabled': True,
            'nativeBoundingBox': {
                'minx': bbox_native[0],
                'maxx': bbox_native[1],
                'miny': bbox_native[2],
                'maxy': bbox_native[3],
            },
            'latLonBoundingBox': {
                'minx': bbox_latlong[0],
                'maxx': bbox_latlong[1],
                'miny': bbox_latlong[2],
                'maxy': bbox_latlong[3],
                'crs': srs,
            },
            'srs': srs,
        }
    }
    response = requests.post(
        layer_url,
        headers=headers,
        data=json.dumps(layer_data),
        auth=(GEOSERVER_USER, GEOSERVER_PASSWORD),
    )

    if response.status_code != 201:
        print(f'Failed to create layer: {response.text}')
        return

    # Assign the style to the layer
    style_url = f'{GEOSERVER_URL}/rest/layers/{workspace}:{layer_name}'
    style_data = {
        'layer': {
            'defaultStyle': {
                'name': style_name,
                'workspace': workspace,
            },
        },
    }
    response = requests.put(
        style_url,
        headers=headers,
        data=json.dumps(style_data),
        auth=(GEOSERVER_USER, GEOSERVER_PASSWORD),
    )

    if response.status_code != 200:
        print(f'Failed to assign style to layer: {response.text}')
        return

    print(f'Layer {layer_name} created and style {style_name} assigned')


def create_layer_group(workspace, group_name, layer_names):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Create the layer group
    group_url = f'{GEOSERVER_URL}/rest/workspaces/{workspace}/layergroups'
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
        auth=(GEOSERVER_USER, GEOSERVER_PASSWORD),
    )

    if response.status_code != 201:
        print(f'Failed to create layer group: {response.text}')
        return

    print(f'Layer group {group_name} created with layers {", ".join(layer_names)}')

# Example usage:
create_layer_group('indrz', 'your_layer_group', ['layer1', 'layer2', 'layer3'])



# Example usage:
create_layer(
    'indrz',
    'your_datastore',
    'your_new_layer',
    'your_existing_sld_style',
    'EPSG:3857',
    (-20037508.34, 20037508.34, -20037508.34, 20037508.34),
    (-180, 180, -85.06, 85.06),
)
