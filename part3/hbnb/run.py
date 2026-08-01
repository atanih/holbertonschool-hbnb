#!/usr/bin/python3
"""Entry point of the HBnB application."""
from app import create_app, db

app = create_app('config.DevelopmentConfig')


@app.shell_context_processor
def make_shell_context():
    """Expose db and models inside `flask shell`."""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
    return {'db': db, 'User': User, 'Place': Place,
            'Review': Review, 'Amenity': Amenity}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
