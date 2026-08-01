from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating 1-5'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    def get(self):
        """Retrieve list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'place_id': review.place.id if review.place else None, 'user_id': review.user.id if review.user else None} for review in reviews], 200

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload

        place = facade.get_place(review_data['place_id'])
        user = facade.get_user(review_data['user_id'])
        
        if not place:
            return {'error': 'Place not found'}, 400
        if not user:
            return {'error': 'User not found'}, 400

        review_data['place'] = place
        review_data['user'] = user
        new_review = facade.create_review(review_data)
        return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating, 'place_id': new_review.place.id, 'user_id': new_review.user.id}, 201

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'place_id': review.place.id if review.place else None, 'user_id': review.user.id if review.user else None}, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update review information"""
        review_data = api.payload

        review = facade.update_review(review_id, review_data)
        if not review:
            return {'error': 'Review not found'}, 404

        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'place_id': review.place.id if review.place else None, 'user_id': review.user.id if review.user else None}, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200