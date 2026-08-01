#!/usr/bin/python3
"""User model with bcrypt password hashing."""
import re
from sqlalchemy.orm import validates
from app import db, bcrypt
from app.models.base_model import BaseModel

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


class User(BaseModel):
    """A registered user of the platform."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # One-to-many: a user owns many places / writes many reviews
    places = db.relationship('Place', backref='owner', lazy=True,
                             cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True,
                              cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email,
                 password=None, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = self.validate_name(first_name, 'first_name')
        self.last_name = self.validate_name(last_name, 'last_name')
        self.email = self.validate_email(email)
        self.is_admin = bool(is_admin)
        if password:
            self.hash_password(password)

    # ---- SQLAlchemy validators: also run on UPDATE, not only on create ----
    @validates('first_name')
    def _check_first_name(self, key, value):
        return self.validate_name(value, 'first_name')

    @validates('last_name')
    def _check_last_name(self, key, value):
        return self.validate_name(value, 'last_name')

    @validates('email')
    def _check_email(self, key, value):
        return self.validate_email(value)

    # ---------- validation ----------
    @staticmethod
    def validate_name(value, field):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError(f'{field} is required and must be <= 50 chars')
        return value

    @staticmethod
    def validate_email(value):
        if not value or not EMAIL_RE.match(value):
            raise ValueError('Invalid email format')
        return value

    # ---------- password ----------
    def hash_password(self, password):
        """Hash the plain password with bcrypt before storing it."""
        if not password or len(password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Compare a plain password against the stored hash."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    # ---------- serialization ----------
    def to_dict(self):
        """Serialize WITHOUT the password field."""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return data
