#!/usr/bin/python3
""" Module for amenities."""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects."""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def gets_amenity(amenity_id):
    """ Retrieves a amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def deletes_amenity(amenity_id):
    """ Deletes a amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def creates_amenity():
    """ Creates amenity."""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def updates_amenity(amenity_id):
    """ Updates a amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()

    return jsonify(amenity.to_dict())
