#!/usr/bin/python3
""" Module for cities."""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves the list of all city objects."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def gets_city(city_id):
    """ Retrieves city object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletes_city(city_id):
    """ Deletes city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def creates_city(state_id):
    """ Creates city."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    city = City(**data)
    city.state_id = state_id
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updates_city(city_id):
    """ Updates city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
