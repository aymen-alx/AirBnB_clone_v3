#!/usr/bin/python3
"""User object"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET', 'POST'])
def all_users():
    """  """
    if request.method == 'GET':
        res = []
        for value in storage.all('User').values():
            res.append(value.to_dict())
        return make_response(jsonify(res))

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('password') is None:
            abort(400, 'Missing password')
        if data.get('email') is None:
            abort(400, 'Missing email')
        new_state_obj = User(**data)
        new_state_obj.save()
        return make_response(jsonify(new_state_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET',
                 'DELETE', 'PUT'])
def user_by_id(user_id):
    """  """
    if request.method == 'GET':
        res = storage.get('User', user_id)
        if res is not None:
            return make_response(jsonify(res.to_dict()))
        abort(404)

    if request.method == 'DELETE':
        del_obj = storage.get('User', user_id)
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
        ignore = ['id', 'email', 'created_at', 'updated_at']
        update_obj = storage.get('User', user_id)
        if update_obj is not None:
            for key, value in data.items():
                if key not in ignore:
                    setattr(update_obj, key, value)
            storage.save()
            return make_response(jsonify(update_obj.to_dict()), 200)
        else:
            abort(404)
