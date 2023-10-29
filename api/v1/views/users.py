#!/usr/bin/python3
""" Module for users."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all User objects."""
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route(
        '/api/v1/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def gets_user(user_id):
    """ Retrieves a User object."""
    user = User.query.get(user_id)
    if user is None:
        abort(404, "User not found")
    return jsonify(user.to_dict())


@app_views.route(
        '/api/v1/users/<int:user_id>', methods=['DELETE'],
        strict_slashes=False)
def deletes_user(user_id):
    """ Deletes a User object."""
    user = User.query.get(user_id)
    if user is None:
        abort(404, "User not found")
    user.delete()
    return jsonify({})


@app_views.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def creates_user():
    """ Creates a user."""
    data = request.get_json()
    if data is None:
        abort(400 "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
        '/api/v1/users/<int:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object."""
    user = User.query.get(user_id)
    if user is None:
        abort(404, "User not found")

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key in ['id', 'email', 'created_at', 'updated_at']:
        data.pop(key, None)

    for key, value in data.items():
        setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict())