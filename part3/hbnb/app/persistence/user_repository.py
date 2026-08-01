#!/usr/bin/python3
"""User-specific repository (Task 6)."""
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository with user-specific queries."""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Return the user matching an email, or None."""
        return self.model.query.filter_by(email=email).first()
