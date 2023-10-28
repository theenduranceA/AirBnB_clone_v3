#!/usr/bin/python3
""" Modules for Reviews."""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews(place_id):
    place = Place.get(place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = Review.get(place_id)
        return jsonify([review.to_dict() for review in reviews])

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        user = User.get(data['user_id'])
        if user is None:
            abort(404)
        if 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400

        review = Review(**data)
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review(review_id):
    review = Review.get(review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, key, value)

        review.save()
        return jsonify(review.to_dict()), 200

    if request.method == 'DELETE':
        review.delete()
        return jsonify({}), 200
