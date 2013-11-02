from flask import Flask, url_for
import os

oxfloodnet = Flask(__name__)

# Determines the destination of the build. Only usefull if you're using Frozen-Flask
oxfloodnet.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
oxfloodnet.jinja_env.globals['static'] = (
	lambda filename: url_for('static', filename = filename)
)

# Data source config
try:
    oxfloodnet.config['FLOOD_DATA_API_URL'] = os.environ['FLOOD_DATA_API_URL']
    oxfloodnet.config['FLOOD_DATA_API_KEY'] = os.environ['FLOOD_DATA_API_KEY']
except KeyError, e:
    raise Exception, "You must define the environment variable %s before running, with e.g. 'export %s=...'" % (e,e)

from oxfloodnet import views
