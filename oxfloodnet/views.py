#!/usr/bin/env python
# @file views.py
#
# Routing for oxfloodnet

import flask
from httpcache import CachingHTTPAdapter
import requests

from oxfloodnet import oxfloodnet, calc

@oxfloodnet.route('/')
def index():
    """
    Return index HTML for human beings
    """
    return flask.render_template('index.html')

@oxfloodnet.route('/data/<centre>/<sw>/<ne>')
def return_data(**kwargs):
    """
    Return JSON data based on bounding box
    """
    request = dict([(i,calc.parse_latlon(j)) for (i,j) in kwargs.items()])
    api_url = oxfloodnet.config['FLOOD_DATA_API_URL']
    params = {
        'lat': request['centre'][0],
        'lon': request['centre'][1],
        'radius': calc.best_circle_radius(
            request['centre'],
            request['sw'],
            request['ne']
        ),
        'api_key': oxfloodnet.config['FLOOD_DATA_API_KEY'],
        'tag': 'oxflood',
    }
    s = requests.Session()
    s.mount('http://', CachingHTTPAdapter())
    s.mount('https://', CachingHTTPAdapter())

    # Test data?
    if flask.request.args.get('test'):
        import json, os
        raw_data = json.load(open(os.path.dirname(__file__) + "/test_data/example.json"))
    else:
        raw_data = s.get(api_url, params = params).json()

    # Map data into format suitable for heat maps
    data = [{'lat': r["location"]['lat'], 'lon': r["location"]['lon'],
             'value': float(r["datastreams"][0]['current_value']) /
                      float(r["datastreams"][0]['max_value'])}
      # Test data needs filtering by tags
      for r in raw_data["results"] if r.has_key('tags') and 'oxflood' in r['tags']]

    return flask.json.jsonify(request = request, data = data)

@oxfloodnet.route('/test/boundingbox/<centre>/<sw>/<ne>')
def return_parsed_request(**kwargs):
    """
    Parse a bounding box URL similar to the /data call
    """
    request = dict([(i,calc.parse_latlon(j)) for (i,j) in kwargs.items()])
    return flask.json.jsonify(request = request)

@oxfloodnet.route('/test/data/<centre>/<sw>/<ne>')
def return_test_data(**kwargs):
    """
    Return example JSON data based on bounding box
    """
    request = dict([(i,calc.parse_latlon(j)) for (i,j) in kwargs.items()])

    test_data = (
      {'lat': 51.7761, 'lon': -1.264, 'value': 1.0},
      {'lat': 51.7763, 'lon': -1.263, 'value': 0.7},
      {'lat': 51.7765, 'lon': -1.265, 'value': 1.2},
    )
    return flask.json.jsonify(request = request, data = test_data)

@oxfloodnet.route('/test/distance/<a>/<b>')
def return_a_to_b(**kwargs):
    """
    Return JSON data giving a distance between two points
    """
    request = dict([(i,calc.parse_latlon(j)) for (i,j) in kwargs.items()])
    distance = calc.haversine(request['a'][1], request['a'][0], request['b'][1], request['b'][0])
    return flask.json.jsonify(request = request, distance = distance)

@oxfloodnet.errorhandler(calc.MalformedLatLon)
def handle_invalid_latlon(error):
    """
    Handle a badly formatted lat/lon comma-separated pair
    """
    response = flask.json.jsonify({"error": error.message})
    response.status_code = error.status_code
    return response
