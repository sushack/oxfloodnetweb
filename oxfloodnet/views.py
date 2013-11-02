#!/usr/bin/env python
# @file views.py
#
# Routing for oxfloodnet

from flask import render_template, json
from oxfloodnet import oxfloodnet

@oxfloodnet.route('/')
def index():
    """
    Return index HTML for human beings
    """
    return render_template('index.html')

@oxfloodnet.route('/data/<ne>/<sw>')
def return_data(ne, sw):
    """
    Return JSON data based on bounding box
    """
    return json.jsonify(request = {'ne':ne,'sw':sw})
