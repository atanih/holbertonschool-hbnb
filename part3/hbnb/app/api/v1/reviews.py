#!/usr/bin/python3
"""Review endpoints with ownership + business rules (Tasks 3 and 4)."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data / Already reviewed')
    @api.response(400, 'You cannot review your own place')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def post(self):
        """Create a review.

        Rules: cannot review your own place, and only one review per place.
        """
        current_user_id = get_jwt_identity()
        data = dict(api.payload)
        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400
        if facade.get_review_by_user_and_place(current_user_id, place.id):
            return {'error': 'You have already reviewed this place'}, 400

        data['user_id'] = current_user_id
        try:
            review = facade.create_review(data)
        except ValueError as exc:
            return {'error': str(exc)}, 400
        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """PUBLIC: list all reviews."""
        return [r.to_dict() for r in facade.get_all_reviews()], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """PUBLIC: get a review by id."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def put(self, review_id):
        """Update a review. Author only, or any admin."""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.update_review(review_id, dict(api.payload))
        except ValueError as exc:
            return {'error': str(exc)}, 400
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review. Author only, or any admin."""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
