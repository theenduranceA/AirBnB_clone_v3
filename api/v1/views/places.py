#!/usr/bin/python3
"""Modules for places."""

from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def gets_place(place_id):
    """ Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def deletes_place(place_id):
    """ Deletes a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def creates_place(city_id):
    """ Creates a Place."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updates_place(place_id):
    """Updates a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def searches_place_objects():
    """ Retrieves all Place object."""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places)

    my_places = []

    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            my_places.append(state.cities)

    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            my_places.append(city.places)

    if not my_places:
        my_places = (storage.all(Place).values())

    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            my_places = [
                    place for place in my_places if amenity in place.amenities]

    places = [place.to_dict(exclude=['amenities']) for place in my_places]

    return jsonify(places)
