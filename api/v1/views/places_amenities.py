#!/usr/bin/python3
"""
"""
from models.amenity import Amenity
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from os import getenv


database = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenity_by_place(place_id):
    """  """
    res = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if database == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    for value in amenities:
        res.append(value.to_dict())
    return jsonify(res)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def delete_place_amenity(place_id, amenity_id):
    """  """
    if request.method == 'DELETE':
        place = storage.get('Place', place_id)
        amenity = storage.get('Amenity', amenity_id)
        if place is None:
            abort(404)
        if amenity is None:
            abort(404)
        if database == "db":
            amenities = place.amenities
        else:
            amenities = place.amenity_ids
        amenities.remove(amenity)
        storage.save()
        return make_response((jsonify({}), 200))

    if request.method == 'POST':
        place = storage.get("Place", place_id)
        amenity = storage.get("Amenity", amenity_id)
        if place is None or amenity is None:
            abort(404)
        if database == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity in place_amenities:
            return jsonify(amenity.to_dict())
        place_amenities.append(amenity)
        place.save()
        return make_response((jsonify(amenity.to_dict()), 201))
