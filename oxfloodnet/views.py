from flask import render_template
from oxfloodnet import oxfloodnet

@oxfloodnet.route('/')
def index():
	return render_template('index.html')
