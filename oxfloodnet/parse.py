#!/usr/bin/env python
# @file parse.py
#
# Parsing input

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

    try:
        latlon = latlon_string.split(',')
    except IndexError:
        raise MalformedLatLon("Malformed lat/lon: %s" % latlon_string)

    try:
        return [ float(ll) for ll in latlon ]
    except ValueError:
        raise MalformedLatLon("Malformed lat/lon: %s" % latlon_string)
