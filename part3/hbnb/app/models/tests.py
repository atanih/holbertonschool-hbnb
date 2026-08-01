from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    user = User(first_name="Antonio", last_name="Torres", email="antonio.torres@gmail.com")
    assert user.first_name == "Antonio"
    assert user.last_name == "Torres"
    assert user.email == "antonio.torres@gmail.com"
    assert user.is_admin is False
    print("User creation test passed!")

def test_place_creation():
    owner = User(first_name="Hinata", last_name="Torres", email="hinata.torres@gmail.com")
    place = Place(title="Apartamento PH en Urb Los Prados", description="Penthouse bien chevere en Los Prados, Caguas Puerto Rico", price=900, latitude=18.2448, longitude=-66.0453, owner=owner)
    review = Review(text="Wepa, estuvo brutal el sitio, lo recomiendo 100%!", rating=5, place=place, user=owner)
    place.add_review(review)
    assert place.title == "Apartamento PH en Urb Los Prados"
    assert place.price == 900
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Wepa, estuvo brutal el sitio, lo recomiendo 100%!"
    print("Place creation and relationship test passed!")

def test_amenity_creation():
    amenity = Amenity(name="Pool")
    assert amenity.name == "Pool"
    print("Amenity creation test passed!")

test_user_creation()
test_place_creation()
test_amenity_creation()