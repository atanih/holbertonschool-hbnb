#!/usr/bin/python3
"""Minimal end-to-end checks for Part 3."""
import unittest
from app import create_app, db
from app.models.user import User


class AuthFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        admin = User('Admin', 'HBnB', 'admin@hbnb.io',
                     password='admin1234', is_admin=True)
        db.session.add(admin)
        user = User('John', 'Doe', 'john@hbnb.io', password='secret123')
        db.session.add(user)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self, email, password):
        res = self.client.post('/api/v1/auth/login',
                               json={'email': email, 'password': password})
        return res.get_json().get('access_token')

    def test_password_is_hashed(self):
        user = User.query.filter_by(email='john@hbnb.io').first()
        self.assertNotEqual(user.password, 'secret123')
        self.assertTrue(user.verify_password('secret123'))

    def test_password_never_returned(self):
        res = self.client.get('/api/v1/users/')
        self.assertNotIn('password', res.get_json()[0])

    def test_login_ok_and_ko(self):
        self.assertIsNotNone(self.login('john@hbnb.io', 'secret123'))
        res = self.client.post('/api/v1/auth/login',
                               json={'email': 'john@hbnb.io',
                                     'password': 'wrong'})
        self.assertEqual(res.status_code, 401)

    def test_protected_requires_token(self):
        self.assertEqual(self.client.get('/api/v1/auth/protected').status_code,
                         401)

    def test_only_admin_creates_amenity(self):
        token = self.login('john@hbnb.io', 'secret123')
        res = self.client.post('/api/v1/amenities/', json={'name': 'WiFi'},
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 403)
        token = self.login('admin@hbnb.io', 'admin1234')
        res = self.client.post('/api/v1/amenities/', json={'name': 'WiFi'},
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 201)

    def test_cannot_review_own_place(self):
        token = self.login('john@hbnb.io', 'secret123')
        h = {'Authorization': f'Bearer {token}'}
        place = self.client.post('/api/v1/places/', headers=h, json={
            'title': 'Loft', 'price': 100.0,
            'latitude': 40.0, 'longitude': -3.0}).get_json()
        res = self.client.post('/api/v1/reviews/', headers=h, json={
            'text': 'Mine', 'rating': 5, 'place_id': place['id']})
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
