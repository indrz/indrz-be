#indrz API Documentation

Welcome to the indrz api documentation.  If you want to use the indrz cloud hosting or host it your self these instructions and words are for you, so please read along.

## Authentication

To access your content on the indrz.com cloud platform you need a valid TOKEN.  This ensures the saftey of your data, so you control who has access to your data.  The Authorization token must be passed along in the header.  If you are hosting your own instance of indrz we highly recommend you do the same and get an SSL Certificate to ensure the saftey of your own instance and API.

    curl -X GET https://www.indrz.com/api/v1/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6tt9k'
    
 
Authentication is built using the Django Rest Framework http://www.django-rest-framework.org/  for more information please visit there wonderful documentation.  

## Documentation conventions
 - Parameters are shown in curly braces, for example **{someValue}**
 - Separate each parameter the   **&**   symbol
 
## API Versioning
Version number is passed inside the URL to help maintain backward compatibility, `v1` defines the version, in this case `1`.

```
http://www.indrz.com/api/v1/
```

## Zoom to a building
Start the map zoomed to the extent of a single building.  The {zoom} parameter is optional.

    http://www.indrz.com/map/building/{building-id}&zoom=18
    
URL Parameter | value | required | description
--- | --- | --- | ---
`buildingid` | integer | yes | Defines the building to zoom to
`zoom` | integer | no | Set custom zoom level to show building
    
Example call:

    http://www.indrz.com/map/building/1&zoom=18

## Zoom to a campus area
A campus area is defined as a POLYGON representing the area in which one or more buildings are grouped with the same name.  Calling zoom to campus will
take the user directly to the extent of the campus polygon.

    http://www.indrz.com/map/campus/{campus-id}&zoom={zooom-value}

URL Parameter | value | required | description
--- | --- | --- | ---
`campusid` | integer | yes | Defines the campus area to zoom to
`zoom` | integer | no | Set custom zoom level to show building accepts values from 0-22

Example call:

    http://www.indrz.com/map/campus/1
    
## Zoom to a specific room location
Zoom the map to a specific indoor space polygon such as a room or office location

    http://www.indrz.com/map/space/{space-id}&zoom={zooom-value}
  
URL Parameter | value | required | description
--- | --- | --- | ---
`spaceid` | integer | yes | Defines the space area to zoom to such as a single office space
`zoom` | integer | no | Set custom zoom level accepts values from 0-22

Example call:

    http://www.indrz.com/map/space/1&zoom=20

## Embedding an indrz indoor map using an iframe

Here we explain how to include an indrz map in your homepage.

Simply create an iframe with the following link

```html
<iframe src="http://www.indrz.com/map/embed/{MapName}">
  width="100%" height="420" frameborder="0" marginheight="0" marginwidth="0"
  scrolling="no"></iframe>
```

replace {MapName}  with the name of the map you want to add

## Get a list of available maps and coresponding names  

    /api/v1/map/list


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

    https://www.indrz.com/api/v1/directions/building=1&startid=234&endid=456

or passing the room name

    http://localhost:8000/api/v1/directions/building=1&startid=307: Orne&endid=311: Mayenne
    
#### Response is GeoJSON LineString Feature Collection
Your response is a GeoJSON LineString showing a 2D line for the entire route.

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "geometry": {
                "coordinates": [
                    [
                        -168564.938764811,
                        5983882.0889364,
                        3
                    ],
                    [
                        -168568.729005951,
                        5983878.03527752,
                        3
                    ]
                ],
                "type": "LineString"
            },
            "type": "Feature",
            "properties": {
                "length": 5.5496016329234,
                "floor": 3,
                "network_type": 0
            }
        },
        {
            "geometry": {
            ...
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




