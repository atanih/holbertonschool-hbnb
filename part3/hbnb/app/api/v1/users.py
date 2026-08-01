#!/usr/bin/python3
"""User endpoints (Tasks 1, 3, 4)."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Plain password')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email (admin only)'),
    'password': fields.String(description='Password (admin only)'),
    'is_admin': fields.Boolean(description='Admin flag (admin only)')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered / Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def post(self):
        """Create a new user. ADMIN ONLY (Task 4)."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        if facade.get_user_by_email(data.get('email')):
            return {'error': 'Email already registered'}, 400
        try:
            user = facade.create_user(data)
        except ValueError as exc:
            return {'error': str(exc)}, 400
        # Password is NEVER returned
        return {'id': user.id, 'message': 'User successfully created'}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Public: list all users (without passwords)."""
        return [u.to_dict() for u in facade.get_all_users()], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Public: get a user by id (password never included)."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input / Email already in use')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def put(self, user_id):
        """Update a user.

        - Regular user: only their own account, and NOT email/password.
        - Admin: any account, including email and password.
        """
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        data = dict(api.payload)

        if not is_admin:
            if current_user_id != user_id:
                return {'error': 'Unauthorized action'}, 403
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400
            data.pop('is_admin', None)
        else:
            new_email = data.get('email')
            if new_email:
                existing = facade.get_user_by_email(new_email)
                if existing and existing.id != user_id:
                    return {'error': 'Email already in use'}, 400

        if not facade.get_user(user_id):
            return {'error': 'User not found'}, 404
        try:
            user = facade.update_user(user_id, data)
        except ValueError as exc:
            return {'error': str(exc)}, 400
        return user.to_dict(), 200
