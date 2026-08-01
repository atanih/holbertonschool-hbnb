-- =====================================================================
-- HBnB - Task 9: CRUD verification script
-- Run AFTER schema.sql and initial_data.sql
-- =====================================================================

-- ---------- READ: initial data is present
SELECT '--- users ---' AS step;
SELECT id, email, is_admin FROM users;

SELECT '--- amenities ---' AS step;
SELECT id, name FROM amenities;

-- ---------- CREATE: a place owned by the admin
INSERT INTO places (id, title, description, price, latitude, longitude,
                    owner_id, created_at, updated_at)
VALUES ('11111111-1111-1111-1111-111111111111', 'Cozy Loft',
        'A nice loft downtown', 120.00, 40.4168, -3.7038,
        '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ---------- CREATE: link two amenities to that place
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('11111111-1111-1111-1111-111111111111',
 '1d8e0da4-c4df-4af7-88ec-1ce29ed8d28e'),
('11111111-1111-1111-1111-111111111111',
 '90db8ab6-3156-4551-94a3-a39fec48235b');

-- ---------- CREATE: a second user + a review on the place
INSERT INTO users (id, first_name, last_name, email, password, is_admin,
                   created_at, updated_at)
VALUES ('22222222-2222-2222-2222-222222222222', 'John', 'Doe',
        'john@hbnb.io', 'not-a-real-hash', FALSE,
        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO reviews (id, text, rating, user_id, place_id,
                     created_at, updated_at)
VALUES ('33333333-3333-3333-3333-333333333333', 'Great stay!', 5,
        '22222222-2222-2222-2222-222222222222',
        '11111111-1111-1111-1111-111111111111',
        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ---------- READ: join across every table
SELECT '--- place with owner, amenities and reviews ---' AS step;
SELECT p.title, u.email AS owner, a.name AS amenity, r.rating
FROM places p
JOIN users u        ON u.id = p.owner_id
LEFT JOIN place_amenity pa ON pa.place_id = p.id
LEFT JOIN amenities a      ON a.id = pa.amenity_id
LEFT JOIN reviews r        ON r.place_id = p.id;

-- ---------- UPDATE
UPDATE places SET price = 150.00
WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT '--- after update ---' AS step;
SELECT title, price FROM places;

-- ---------- DELETE (cascade removes the review and the links)
DELETE FROM places WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT '--- after delete: reviews left ---' AS step;
SELECT COUNT(*) AS remaining_reviews FROM reviews;
SELECT '--- after delete: place_amenity left ---' AS step;
SELECT COUNT(*) AS remaining_links FROM place_amenity;
