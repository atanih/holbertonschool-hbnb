#!/usr/bin/python3
"""Facade: single entry point between the API layer and persistence."""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository


class HBnBFacade:
    """Business logic facade backed by SQLAlchemy repositories."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ------------------------------------------------------------- USERS
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        password = data.pop('password', None)
        if 'email' in data:
            User.validate_email(data['email'])
        user = self.user_repo.update(user_id, data)
        if password:
            user.hash_password(password)
            user.save()
        return user

    # --------------------------------------------------------- AMENITIES
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    # ------------------------------------------------------------ PLACES
    def create_place(self, place_data):
        amenity_ids = place_data.pop('amenities', []) or []
        place = Place(**place_data)
        for aid in amenity_ids:
            amenity = self.amenity_repo.get(aid)
            if amenity:
                place.amenities.append(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        amenity_ids = data.pop('amenities', None)
        data.pop('owner_id', None)
        place = self.place_repo.update(place_id, data)
        if place and amenity_ids is not None:
            place.amenities = [
                a for a in (self.amenity_repo.get(i) for i in amenity_ids) if a
            ]
            place.save()
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ----------------------------------------------------------- REVIEWS
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_reviews_by_place(place_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        return self.review_repo.get_review_by_user_and_place(
            user_id, place_id)

    def update_review(self, review_id, data):
        data.pop('user_id', None)
        data.pop('place_id', None)
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
