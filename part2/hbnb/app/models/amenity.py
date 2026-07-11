from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        # Validation
        if not name or len(name) > 50:
            raise ValueError("Name is required and must be under 50 characters")

        self.name = name