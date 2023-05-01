#!/usr/bin/python3
""" status """
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response


@app_views.route('/status')
def status():
    """  """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def obj_status():
    """  """
    res = {}
    object_format = {
        'Amenity': 'amenities',
        'City': 'cities',
        'Place': 'places',
        'Review': 'reviews',
        'State': 'states',
        'User': 'users'
    }
    for key, value in object_format.items():
        res[value] = storage.count(key)
    return jsonify(res)
