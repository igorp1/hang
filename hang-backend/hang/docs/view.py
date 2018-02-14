from . import docs
from endpoints import api_endpoints
from flask import render_template

@docs.route('/', methods=['GET'])
def index():
    return render_template('index.html', endpoins=api_endpoints)