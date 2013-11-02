#!/usr/bin/env python
# @file calculation.py
#
# Parsing input and calculating spherical results

class MalformedData(Exception):
    """
    Raise exception if incoming data is malformed
    """

    status_code = 400
    message_template = "Malformed data: %s"

    def __init__(self, data):
        Exception.__init__(self)
        self.message = self.message_template % data

class MalformedLatLon(MalformedData):
    """
    Raise exception if latitude/longitude pair is malformed
    """

    message_template = "Malformed latitude/longitude pair: %s"

def parse_latlon(latlon_string):
    """
    Parse a lat/lon comma-separated string into two floats
    """

    # Split on comma and ensure we've got two values
    try:
        latlon = latlon_string.split(',')
        latlon[1]
    except IndexError:
        raise MalformedLatLon("Malformed lat/lon: %s" % latlon_string)

    # Turn each value into a float
    try:
        return [ float(ll) for ll in latlon ]
    except ValueError:
        raise MalformedLatLon("Malformed lat/lon: %s" % latlon_string)

def best_circle_radius(centre, sw, ne):
    """
    Calculate the minimum circle, centred on centre, which encompasses
    both sw and ne. Our bounding box will fit into this circle, even
    assuming our box is distorted by curvature of the earth.
    """

    # Above the equator, centre<->sw is the bigger distance
    # Below the equator, centre<->ne is the bigger distance
    # Use the bigger one, to ensure we encapsulate the smaller
    non_centre = sw if (centre[0] > 0) else ne

    # Haversine formula takes lon/lat, not lat/lon
    return haversine(centre[1], centre[0], non_centre[1], non_centre[0])

# http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
# Seems legit
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km 
