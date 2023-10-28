#!/usr/bin/python3
"""Modules for places."""

from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    place.delete()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'message': 'Missing user_id'}), 400
    user = User.get(data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        return jsonify({'message': 'Missing name'}), 400
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Not a JSON'}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
