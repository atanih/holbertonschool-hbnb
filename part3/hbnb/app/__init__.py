#!/usr/bin/python3
"""Application Factory for the HBnB API."""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in 'Bearer <JWT>' to authorize."
    }
}


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application.

    Args:
        config_class: dotted path or class object holding the configuration.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Allow the Part 4 web client (served from a different origin) to call
    # this API from the browser.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Imported here to avoid circular imports (models need `db`).
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    @app.route('/api/v1/protected')
    def protected_alias():
        """Alias of /api/v1/auth/protected (task 2 curl example)."""
        from flask_jwt_extended import verify_jwt_in_request
        from flask_jwt_extended import get_jwt_identity, get_jwt
        verify_jwt_in_request()
        return {
            'message': f'Hello, user {get_jwt_identity()}',
            'is_admin': get_jwt().get('is_admin', False)
        }, 200

    return app
