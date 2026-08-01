#!/usr/bin/python3
"""Place model."""
from sqlalchemy.orm import validates
from app import db
from app.models.base_model import BaseModel
from app.models.associations import place_amenity


class Place(BaseModel):
    """A place owned by a user."""

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                         nullable=False)

    # One-to-many: a place has many reviews
    reviews = db.relationship('Review', backref='place', lazy=True,
                              cascade='all, delete-orphan')
    # Many-to-many: a place has many amenities
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id,
                 description=None, **kwargs):
        super().__init__(**kwargs)
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id

    # ---- SQLAlchemy validators: also run on UPDATE, not only on create ----
    @validates('title')
    def _check_title(self, key, value):
        return self.validate_title(value)

    @validates('price')
    def _check_price(self, key, value):
        return self.validate_price(value)

    @validates('latitude')
    def _check_latitude(self, key, value):
        return self.validate_latitude(value)

    @validates('longitude')
    def _check_longitude(self, key, value):
        return self.validate_longitude(value)

    @staticmethod
    def validate_title(value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError('Title is required and must be <= 100 chars')
        return value

    @staticmethod
    def validate_price(value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError('Price must be a number')
        if value <= 0:
            raise ValueError('Price must be a positive number')
        return value

    @staticmethod
    def validate_latitude(value):
        value = float(value)
        if not -90.0 <= value <= 90.0:
            raise ValueError('Latitude must be between -90 and 90')
        return value

    @staticmethod
    def validate_longitude(value):
        value = float(value)
        if not -180.0 <= value <= 180.0:
            raise ValueError('Longitude must be between -180 and 180')
        return value

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })
        return data

    def to_dict_full(self):
        """Detailed representation including owner, amenities and reviews."""
        data = self.to_dict()
        data['owner'] = self.owner.to_dict() if self.owner else None
        data['amenities'] = [a.to_dict() for a in self.amenities]
        data['reviews'] = [r.to_dict() for r in self.reviews]
        return data
