#!/usr/bin/env python
# @file views.py
#
# Routing for oxfloodnet

import flask
from oxfloodnet import oxfloodnet

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
    return flask.json.jsonify(request = {'sw':sw,'ne':ne})
