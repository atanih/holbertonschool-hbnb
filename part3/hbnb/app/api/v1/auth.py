#!/usr/bin/python3
"""Authentication endpoints: login (Task 2)."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity, get_jwt)
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """Authenticate a user and return a JWT access token."""

    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful, token returned')
    @api.response(401, 'Invalid credentials')
    def post(self):
        credentials = api.payload
        user = facade.get_user_by_email(credentials.get('email'))
        if not user or not user.verify_password(credentials.get('password')):
            return {'error': 'Invalid credentials'}, 401

        # identity MUST be a string in flask-jwt-extended >= 4.x
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': bool(user.is_admin)}
        )
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    """Smoke-test endpoint to verify a token is valid."""

    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': claims.get('is_admin', False)
        }, 200
