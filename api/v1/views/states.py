#!/usr/bin/python3
"""Modules for states."""

from flask import Flask, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def gets_state(state_id):
    """ Retrieves a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deletes_state(state_id):
    """ Deletes a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creates_state():
    """ Creates a State object."""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}, 400)
    if 'name' not in data:
        return jsonify({"error": "Missing name"}, 400)
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updates_state(state_id):
    """ Updates the state object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}, 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
