#!/usr/bin/python3
"""
Amenity objects
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    """  """
    if request.method == 'GET':
        res = []
        for value in storage.all(Amenity).values():
            res.append(value.to_dict())
        return jsonify(res)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        elif data.get('name') is None:
            abort(400, 'Missing name')
        new_state_obj = Amenity(**data)
        new_state_obj.save()
        return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE', 'PUT', 'GET'])
def delete_amenity(amenity_id):
    """  """
    if request.method == 'GET':
        response = storage.get('Amenity', amenity_id)
        if response is not None:
            return jsonify(response.to_dict())
        abort(404)

    if request.method == 'DELETE':
        del_obj = storage.get('Amenity', amenity_id)
        if del_obj is not None:
            del_obj.delete()
            storage.save()
            return (jsonify({}), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        elif data.get('name') is None:
            abort(400, 'Missing name')
        ignore = ['id', 'created_at', 'updated_at']
        update_obj = storage.get('Amenity', amenity_id)
        if update_obj is not None:
            for key, value in data.items():
                if key not in ignore:
                    setattr(update_obj, key, value)
            storage.save()
            return (jsonify(update_obj.to_dict()))
        else:
            abort(404)
