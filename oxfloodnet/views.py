#!/usr/bin/env python
# @file views.py
#
# Routing for oxfloodnet

import flask
from oxfloodnet import oxfloodnet
from oxfloodnet import parse

@oxfloodnet.route('/')
def index():
    """
    Return index HTML for human beings
    """
    return flask.render_template('index.html')

@oxfloodnet.route('/data/<sw>/<ne>')
def return_data(ne, sw):
    """
    Return JSON data based on bounding box
    """
    return flask.json.jsonify(request = {'sw': parse.parse_latlon(sw), 'ne': parse.parse_latlon(ne)})

@oxfloodnet.errorhandler(parse.MalformedLatLon)
def handle_invalid_latlon(error):
    """
    Handle a badly formatted lat/lon comma-separated pair
    """
    response = flask.json.jsonify({"error": error.message})
    response.status_code = error.status_code
    return response
