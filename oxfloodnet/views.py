#!/usr/bin/env python
# @file views.py
#
# Routing for oxfloodnet

import flask
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
    return flask.json.jsonify(request = request)

@oxfloodnet.errorhandler(calc.MalformedLatLon)
def handle_invalid_latlon(error):
    """
    Handle a badly formatted lat/lon comma-separated pair
    """
    response = flask.json.jsonify({"error": error.message})
    response.status_code = error.status_code
    return response
