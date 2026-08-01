-- =====================================================================
-- HBnB - Task 9: initial data
-- Admin password below is the bcrypt hash of: admin1234
-- =====================================================================

INSERT INTO users (id, first_name, last_name, email, password, is_admin,
                   created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$bVFD9NfzVYD3RuY50GV7pOcOy1KDYjp7npBO4ow9N2LO5pyfbwedO',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('1d8e0da4-c4df-4af7-88ec-1ce29ed8d28e', 'WiFi',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('90db8ab6-3156-4551-94a3-a39fec48235b', 'Swimming Pool',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('cd5fd33b-0800-4ef1-a945-6ca77897f46b', 'Air Conditioning',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
