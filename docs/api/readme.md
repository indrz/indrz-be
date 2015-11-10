#indrz API Documentation

Welcome to the indrz api documentation.  If you want to use the indrz cloud hosting or host it your self these instructions and words are for you, so please read along.

## Authentication

To access your content on the indrz.com cloud platform you need a valid TOKEN.  This ensures the saftey of your data, so you control who has access to your data.  The Authorization token must be passed along in the header.  If you are hosting your own instance of indrz we highly recommend you do the same and get an SSL Certificate to ensure the saftey of your own instance and API.

    curl -X GET https://www.indrz.com/api/v1/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6tt9k'
    
 
Authentication is built using the Django Rest Framework http://www.django-rest-framework.org/  for more information please visit there wonderful documentation.  

## Documentation conventions
 - Parameters are shown in curly braces, for example **{someValue}**
 - Separate each parameter the   **&**   symbol

## Embedding an indrz indoor map using an iframe

Here we explain how to include an indrz map in your homepage.

Simply create an iframe with the following link

```html
<iframe src="http://www.indrz.com/map/embed/{MapName}">
  width="100%" height="420" frameborder="0" marginheight="0" marginwidth="0"
  scrolling="no"></iframe>
```

replace {MapName}  with the name of the map you want to add

To get a list of all available map names use our API call  

    /api/v1/list-map-names


## Indoor Direction API

The directions api is designed to allow you to show a route from any indoor room location to any other room location within a building complex.

    /api/v1/directions/buildingid={building-id}&startid={room-id}&endid={room-id}&type={route-type-value}
    
    
URL Parameter | value | required | description
--- | --- | --- | ---
`buildingid` | integer | yes | Defines the campus for which you want the buildings
`startid` | integer | yes | Start room id for creating a route
`endid` | integer | yes | Destination room id as end location of route
`type` | integer | no | Sets the routing type, 0 = normal, 1 = barrierierfree(no stairs) default is 0


An example call would look like this:

    https://www.indrz.com/api/v1/directions/buildingid=1&startid=234&endid=456
    
#### Response is GeoJSON LineString Feature Collection
Your response is a GeoJSON LineString showing a 2D line for the entire route.

```json

    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -101.744384765625,
                        39.32155002466662
                    ],
                    [
                        -101.5521240234375,
                        39.330048552942415
                    ],
                    [
                        -101.40380859375,
                        39.330048552942415
                    ]
                ]
            },
            "properties": {
                "floor": -1,
                "type": 0
            }
        }
    ]
}

```

    
### Route from coordinate to coordinate in building

You can create a route for any start end coordinate pair with floor and route_type option

An example runing on your local developer machine with the Django dev server

    http://localhost:8000/api/v1/directions/-168527.958404064,5983885.94934575,-1&-168578.959377896,5983891.19705399,3&0/?format=json
    

## Indoor Space API 

Lets say you want to display a GeoJSON polygon layer on your map of all the rooms, aka spaces from single floor from a single building.

    /api/v1/space/building={building-id}&floor={floor-id}

Example call:

    https://www.indrz.com/api/v1/space/building=45&floor=123

##### Response is JSON

some response

### Indoor Room information

Our indrz indoor room spaces api is designed to zoom a user into a specific room inside a building and show the correct floor level

    /api/v1/space/space=435

This will zoom you to the exact room location on the map.

An example call:

    https://www.indrz.com/api/v1/space/space=435

##### Response is JSON

some response

### Get room centroid

Return the center point of a specified room within a building

    /api/v1/space/centroid=435

This will return a GeoJSON POINT geometry of the rooms geometric center.

An example call:

    https://www.indrz.com/api/v1/space/centroid=435

##### Response is GeoJSON


```json
{
    "type": "Point",
    "coordinates": [
        -105.01621,
        39.57422
    ]
}

```




