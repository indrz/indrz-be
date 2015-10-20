#indrz API Documentation

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

    /api/v1/space/building/building={building-id}&floor={floor-id}

Example call:

    http://www.indrz.com/api/v1/space/building=45&floor=123

#### Response is JSON

some response

### Indoor Room information

Our indrz indoor room spaces api is designed to zoom a user into a specific room inside a building and show the correct floor level

    /api/v1/space/space=435

This will zoom you to the exact room location on the map.

An example call:

    http://www.indrz.com/api/v1/space/space=435

#### Response is JSON

some response




```python
def foo():
    if not bar:
        return True

```



