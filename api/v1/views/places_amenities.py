#!/usr/bin/python3
""" Modulue for Places and Amenity object."""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities_by_place(place_id):
    """ Retrieves the list of all Amenity objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'], strict_slashes=False)
def deletes_amenity_place(place_id, amenity_id):
    """ Deletes a Amenity object to a Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'], strict_slashes=False)
def links_amenity_to_place(place_id, amenity_id):
    """ Link a Amenity object to a Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
