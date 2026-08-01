#!/usr/bin/python3
"""Amenity model."""
from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """An amenity that can be attached to many places."""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = self.validate_name(name)

    @staticmethod
    def validate_name(value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError('Amenity name is required and must be <= 50')
        return value

    def to_dict(self):
        data = super().to_dict()
        data['name'] = self.name
        return data
