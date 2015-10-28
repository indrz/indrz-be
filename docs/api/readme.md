#indrz API Documentation

Welcome to the indrz api documentation.  If you want to use the indrz cloud hosting or host it your self these instructions and words are for you, so please read along.

## Authentication

To access your content on the indrz.com cloud platform you need a valid TOKEN.  This ensures the saftey of your data, so you control who has access to your data.  The Authorization token must be passed along in the header.  If you are hosting your own instance of indrz we highly recommend you do the same and get an SSL Certificate to ensure the saftey of your own instance and API.

    curl -X GET https://www.indrz.com/api/v1/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6tt9k'
    
 
Authentication is built using the Django Rest Framework http://www.django-rest-framework.org/  for more information please visit there wonderful documentation.   

## Indoor Direction API

The directions api is designed to allow you to show a route from any indoor room location to any other room location within a building complex.

    /api/v1/directions/building={building-id}&start={room-id}&destination={room-id}
    
An example call would look like this:

    http://www.indrz.com/api/v1/directions/building=45&start=234&end=456
    
#### Response is GeoJSON
Your response is a GeoJSON LineString showing a 2D line for the entire route.

some response

## Indoor Space API 

Lets say you want to display a GeoJSON polygon layer on your map of all the rooms, aka spaces from single floor from a single building.

    /api/v1/space/building={building-id}&floor={floor-id}

Example call:

    http://www.indrz.com/api/v1/space/building=45&floor=123

##### Response is JSON

some response

### Indoor Room information

Our indrz indoor room spaces api is designed to zoom a user into a specific room inside a building and show the correct floor level

    /api/v1/space/space=435

This will zoom you to the exact room location on the map.

An example call:

    http://www.indrz.com/api/v1/space/space=435

##### Response is JSON

some response

### Get room centroid

Return the center point of a specified room within a building

    /api/v1/space/centroid=435

This will return a GeoJSON POINT geometry of the rooms geometric center.

An example call:

    http://www.indrz.com/api/v1/space/centroid=435

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




