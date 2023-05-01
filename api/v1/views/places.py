#!/usr/bin/python3
""" Place objects """
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def place_by_city(city_id):
    """  """
    if request.method == 'GET':
        res = []
        city = storage.get('City', city_id)
        if city is None:
            abort(404)
        for value in city.places:
            res.append(value.to_dict())
        return make_response(jsonify(res))

    if request.method == 'POST':
        city = storage.get('City', city_id)
        data = request.get_json()
        if city is None:
            abort(404)
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('user_id') is None:
            abort(400, 'Missing user_id')
        if data.get('name') is None:
            abort(400, 'Missing name')
        user = storage.get('User', data['user_id'])
        if user is None:
            abort(404)
        data['city_id'] = city_id
        new_state_obj = Place(**data)
        new_state_obj.save()
        return make_response(jsonify(new_state_obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place_by_id(place_id):
    """  """
    if request.method == 'GET':
        res = storage.get(Place, place_id)
        if res is not None:
            return make_response(jsonify(res.to_dict()))
        abort(404)

    if request.method == 'DELETE':
        del_obj = storage.get(Place, place_id)
        if del_obj is not None:
            del_obj.delete()
            storage.save()
            return make_response((jsonify({}), 200))
        else:
            abort(404)

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        update_obj = storage.get('Place', place_id)
        if update_obj is not None:
            for key, value in data.items():
                if key not in ignore:
                    setattr(update_obj, key, value)
            storage.save()
            return make_response(jsonify(update_obj.to_dict()), 200)
        else:
            abort(404)
