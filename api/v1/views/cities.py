#!/usr/bin/python3
"""
City objects
"""
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def city_by_state(state_id):
    """  """
    if request.method == 'GET':
        res = []
        states = storage.get('State', state_id)
        if states is None:
            abort(404)

        cities = storage.all('City')
        for city in cities.values():
            if city.state_id == state_id:
                res.append(city.to_dict())
        return make_response(jsonify(res))

    if request.method == 'POST':
        state = storage.get('State', state_id)
        data = request.get_json()
        if state is None:
            abort(404)
        if data is None:
            abort(400, 'Not a JSON')
        elif data.get('name') is None:
            abort(400, 'Missing name')
        data['state_id'] = state_id
        new_state_obj = City(**data)
        new_state_obj.save()
        return make_response(jsonify(new_state_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_by_id(city_id):
    """  """
    if request.method == 'GET':
        res = storage.get('City', city_id)
        if res is not None:
            return make_response(jsonify(res.to_dict()))
        abort(404)

    if request.method == 'DELETE':
        del_obj = storage.get('City', city_id)
        if del_obj is not None:
            del_obj.delete()
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        elif data.get('name') is None:
            abort(400, 'Missing name')

        update_obj = storage.get('City', city_id)
        if update_obj is not None:
            update_obj.name = data.get('name')
            storage.save()
            return make_response(jsonify(update_obj.to_dict()))
        else:
            abort(404)
