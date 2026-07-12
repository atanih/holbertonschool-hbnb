import unittest
import json
from app import create_app

class TestHBnBAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            'first_name': 'Juan',
            'last_name': 'García',
            'email': 'juan.garcia@gmail.com'
        }
        response = self.client.post('/api/v1/users/', 
                                    data=json.dumps(user_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Juan')
        self.assertIn('id', data)

    def test_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_create_amenity(self):
        """Test creating a new amenity"""
        amenity_data = {'name': 'Wi-Fi'}
        response = self.client.post('/api/v1/amenities/',
                                    data=json.dumps(amenity_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_create_place(self):
        """Test creating a place"""
        # Primero crear un usuario (owner)
        user_data = {
            'first_name': 'María',
            'last_name': 'López',
            'email': 'maria.lopez@gmail.com'
        }
        user_response = self.client.post('/api/v1/users/',
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        user_id = json.loads(user_response.data)['id']
        
        # Crear place
        place_data = {
            'title': 'Apartamento PH en Urb Los Prados',
            'description': 'Penthouse bien chevere en Los Prados, Caguas Puerto Rico',
            'price': 900,
            'latitude': 18.2448,
            'longitude': -66.0453,
            'owner_id': user_id
        }
        response = self.client.post('/api/v1/places/',
                                    data=json.dumps(place_data),
                                    content_type='application/json')
        
        if response.status_code != 201:
            print("Error response:", response.data)
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Apartamento PH en Urb Los Prados')
        self.assertEqual(data['price'], 900)

    def test_create_review(self):
        """Test creating a review"""
        # Crear usuario
        user_data = {
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'email': 'carlos.rodriguez@gmail.com'
        }
        user_response = self.client.post('/api/v1/users/',
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        user_id = json.loads(user_response.data)['id']
        
        # Crear place
        place_data = {
            'title': 'Casa en San Juan',
            'description': 'Hermosa casa en el corazón de San Juan',
            'price': 1500,
            'latitude': 18.3892,
            'longitude': -66.1195,
            'owner_id': user_id
        }
        place_response = self.client.post('/api/v1/places/',
                                          data=json.dumps(place_data),
                                          content_type='application/json')
        
        if place_response.status_code != 201:
            print("Place Error response:", place_response.data)
        
        place_id = json.loads(place_response.data)['id']
        
        # Crear review
        review_data = {
            'text': 'Wepa, estuvo brutal el sitio, lo recomiendo 100%!',
            'rating': 5,
            'place_id': place_id,
            'user_id': user_id
        }
        response = self.client.post('/api/v1/reviews/',
                                    data=json.dumps(review_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['rating'], 5)

    def test_delete_review(self):
        """Test deleting a review"""
        # Crear usuario, place y review primero
        user_data = {'first_name': 'José', 'last_name': 'Martínez', 'email': 'jose@gmail.com'}
        user_response = self.client.post('/api/v1/users/', data=json.dumps(user_data), content_type='application/json')
        user_id = json.loads(user_response.data)['id']
        
        place_data = {'title': 'Casa', 'description': 'Casa bonita', 'price': 1000, 'latitude': 18.0, 'longitude': -66.0, 'owner_id': user_id}
        place_response = self.client.post('/api/v1/places/', data=json.dumps(place_data), content_type='application/json')
        
        if place_response.status_code != 201:
            print("Place Delete Error:", place_response.data)
        
        place_id = json.loads(place_response.data)['id']
        
        review_data = {'text': 'Bueno', 'rating': 4, 'place_id': place_id, 'user_id': user_id}
        review_response = self.client.post('/api/v1/reviews/', data=json.dumps(review_data), content_type='application/json')
        review_id = json.loads(review_response.data)['id']
        
        # Deletear review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()