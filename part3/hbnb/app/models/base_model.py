#!/usr/bin/python3
"""BaseModel mapped to SQLAlchemy: common columns for every entity."""
import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Abstract base: id (UUID4), created_at, updated_at."""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Persist the object and refresh updated_at."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update attributes from a dict, ignoring unknown keys."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ('id', 'created_at'):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Serialize the common attributes."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat()
            if self.created_at else None,
            'updated_at': self.updated_at.isoformat()
            if self.updated_at else None
        }
