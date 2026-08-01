#!/usr/bin/python3
"""Review model."""
from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """A review written by a user about a place."""

    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                        nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'),
                        nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id',
                            name='unique_user_place_review'),
        db.CheckConstraint('rating >= 1 AND rating <= 5',
                           name='check_rating_range'),
    )

    def __init__(self, text, rating, user_id, place_id, **kwargs):
        super().__init__(**kwargs)
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.user_id = user_id
        self.place_id = place_id

    @staticmethod
    def validate_text(value):
        if not value or not isinstance(value, str):
            raise ValueError('Review text is required')
        return value

    @staticmethod
    def validate_rating(value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError('Rating must be an integer')
        if not 1 <= value <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return value

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        return data
