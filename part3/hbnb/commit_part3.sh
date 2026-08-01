#!/bin/bash
# Commits task por task para HBnB Part 3
set -e
cd "$(git rev-parse --show-toplevel)"

git add part3/.gitignore part3/hbnb/requirements.txt
git commit -m "chore(part3): setup environment and dependencies

- add requirements for flask-restx, flask-bcrypt, flask-jwt-extended and flask-sqlalchemy
- ignore venv, __pycache__, database files and secrets"

git add part3/hbnb/config.py part3/hbnb/app/__init__.py part3/hbnb/run.py
git commit -m "feat(task0): application factory now accepts a configuration object

- add DevelopmentConfig, ProductionConfig and TestingConfig
- create_app(config_class) loads config via app.config.from_object
- register bcrypt, jwt and db extensions with the init_app pattern"

git add part3/hbnb/app/models/base_model.py part3/hbnb/app/models/user.py
git commit -m "feat(task1): hash user passwords with bcrypt

- add hash_password() and verify_password() to the User model
- POST /api/v1/users/ accepts and hashes the password field
- password is never included in GET responses"

git add part3/hbnb/app/api/v1/auth.py
git commit -m "feat(task2): JWT authentication with flask-jwt-extended

- POST /api/v1/auth/login returns a signed access token
- is_admin embedded as an additional claim, identity kept as string
- add /auth/protected smoke-test endpoint and Swagger Bearer auth"

git add part3/hbnb/app/api/v1/places.py part3/hbnb/app/api/v1/reviews.py
git commit -m "feat(task3): protect endpoints with JWT and ownership checks

- places: create requires auth, owner taken from the token
- places: update and delete restricted to the owner
- reviews: cannot review your own place, one review per user per place
- public endpoints remain accessible without a token"

git add part3/hbnb/app/api/v1/users.py part3/hbnb/app/api/v1/amenities.py
git commit -m "feat(task4): role-based access control for administrators

- admin-only: create users, create and update amenities
- admins can edit any user including email and password
- admins bypass ownership restrictions on places and reviews
- unique email validation when an admin changes a user's email"

git add part3/hbnb/app/persistence/repository.py part3/hbnb/app/services/
git commit -m "feat(task5): add SQLAlchemyRepository implementing the Repository interface

- keep InMemoryRepository for unit tests
- refactor HBnBFacade to depend on the repository abstraction"

git add part3/hbnb/app/persistence/user_repository.py
git commit -m "feat(task6): map BaseModel and User to SQLAlchemy

- BaseModel as abstract model with UUID id, created_at and updated_at
- User mapped to the users table with unique email and bcrypt password
- add UserRepository with get_user_by_email and wire it into the Facade"

git add part3/hbnb/app/models/place.py part3/hbnb/app/models/review.py part3/hbnb/app/models/amenity.py part3/hbnb/app/persistence/
git commit -m "feat(task7): map Place, Review and Amenity to SQLAlchemy models

- core attributes mapped for each entity
- dedicated repositories for place, review and amenity
- keep Part 2 validation rules for price, coordinates and rating"

git add part3/hbnb/app/models/associations.py part3/hbnb/app/models/
git commit -m "feat(task8): map relationships between entities

- User 1:N Place and User 1:N Review with delete-orphan cascade
- Place 1:N Review
- Place N:M Amenity through the place_amenity association table
- unique (user_id, place_id) and rating range constraints on reviews"

git add part3/hbnb/sql/schema.sql part3/hbnb/sql/initial_data.sql part3/hbnb/sql/test_crud.sql
git commit -m "feat(task9): raw SQL scripts for schema, initial data and CRUD tests

- schema.sql with PK, FK, UNIQUE and CHECK constraints
- initial_data.sql with the admin user and three base amenities
- test_crud.sql verifying insert, join, update and cascade delete"

git add part3/hbnb/sql/er_diagram.mmd part3/hbnb/README.md
git commit -m "docs(task10): add Mermaid ER diagram and Part 3 README

- model users, places, reviews, amenities and place_amenity
- document endpoints, permissions and setup instructions"

git add part3/
git commit -m "test(part3): add authentication flow tests and API verification script" || true

echo
echo "=== historial ==="
git log --oneline -15
