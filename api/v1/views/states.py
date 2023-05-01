#!/usr/bin/python3
"""State objects"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=['GET', 'POST'])
def all_states():
    """  """
    if request.method == 'GET':
        res = []
        for value in storage.all('State').values():
            res.append(value.to_dict())
        return make_response(jsonify(res))

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        elif data.get('name') is None:
            abort(400, 'Missing name')
        new_state_obj = State(**data)
        new_state_obj.save()
        return make_response(jsonify(new_state_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET',
                 'DELETE', 'PUT'])
def state_by_id(state_id):
    """  """
    if request.method == 'GET':
        res = storage.get('State', state_id)
        if res is not None:
            return make_response(jsonify(res.to_dict()))
        abort(404)

    if request.method == 'DELETE':
        del_obj = storage.get('State', state_id)
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
        update_obj = storage.get('State', state_id)
        if update_obj is not None:
            update_obj.name = data.get('name')
            storage.save()
            return (jsonify(update_obj.to_dict()))
        else:
            abort(404)
