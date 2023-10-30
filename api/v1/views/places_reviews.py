#!/usr/bin/python3
""" Module for review."""

from flask import Flask, request, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves a Review object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def gets_review(review_id):
    """ Retrieves a Place object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def deletes_review(review_id):
    """ Deletes a Place object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def creates_review(place_id):
    """ Creates a Review."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updates_review(review_id):
    """ Updates a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
