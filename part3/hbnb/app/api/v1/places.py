#!/usr/bin/python3
"""Place endpoints with ownership checks (Tasks 3 and 4)."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Missing or invalid token')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def post(self):
        """Create a place. Authenticated users only; owner = token identity."""
        current_user_id = get_jwt_identity()
        data = dict(api.payload)
        data['owner_id'] = current_user_id
        try:
            place = facade.create_place(data)
        except ValueError as exc:
            return {'error': str(exc)}, 400
        return place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """PUBLIC: list all places (no token required)."""
        return [p.to_dict() for p in facade.get_all_places()], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """PUBLIC: place details with owner, amenities and reviews."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_full(), 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def put(self, place_id):
        """Update a place. Owner only, or any admin (Task 4 bypass)."""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.update_place(place_id, dict(api.payload))
        except ValueError as exc:
            return {'error': str(exc)}, 400
        return {'message': 'Place updated successfully'}, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place. Owner only, or any admin."""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """PUBLIC: all reviews for a given place."""
        if not facade.get_place(place_id):
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200
