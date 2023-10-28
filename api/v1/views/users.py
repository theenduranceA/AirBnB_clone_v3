#!/usr/bin/python3
""" Module for users."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage
 

@app_views.route('/api/v1/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list), 200

@app_views.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@app_views.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user.delete()
    return jsonify({}), 200

@app_views.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key in ['id', 'email', 'created_at', 'updated_at']:
        data.pop(key, None)

    for key, value in data.items():
        setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
