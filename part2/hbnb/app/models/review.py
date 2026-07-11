from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Validation
        if not text:
            raise ValueError("Text is required")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        if not place:
            raise ValueError("Place is required")
        if not user:
            raise ValueError("User is required")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user