#!/usr/bin/python3
"""
Review object
"""
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def review_by_place(place_id):
    """  """
    if request.method == 'GET':
        res = []
        place = storage.get('Place', place_id)
        if place is None:
            abort(404)
        for review in place.reviews:
            res.append(review.to_dict())
        return make_response(jsonify(res))

    if request.method == 'POST':
        place = storage.get('Place', place_id)
        data = request.get_json()
        if place is None:
            abort(404)
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('user_id') is None:
            abort(400, 'Missing user_id')
        if data.get('text') is None:
            abort(400, 'Missing text')

        user = storage.get('User', data['user_id'])
        if user is None:
            abort(404)
        data['place_id'] = place_id
        new_state_obj = Review(**data)
        new_state_obj.save()
        return make_response(jsonify(new_state_obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['DELETE',
                 'GET', 'PUT'])
def delete_review(review_id):
    """  """
    if request.method == 'DELETE':
        del_obj = storage.get('Review', review_id)
        if del_obj is not None:
            del_obj.delete()
            storage.save()
            return make_response((jsonify({}), 200))
        else:
            abort(404)

    if request.method == 'GET':
        res = storage.get('Review', review_id)
        if res is not None:
            return make_response(jsonify(res.to_dict()))
        abort(404)

    if request.method == 'PUT':
        update_obj = storage.get('Review', review_id)
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if update_obj is not None:
            for key, value in data.items():
                if key not in ignore:
                    setattr(update_obj, key, value)
            storage.save()
            return jsonify(update_obj.to_dict()), 200
        else:
            abort(404)
