-- =====================================================================
-- HBnB - Task 9: full database schema (raw SQL)
-- Compatible with SQLite (development) and MySQL 8 (production).
-- =====================================================================

-- Order matters: drop children before parents.
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- ------------------------------------------------------------- USERS
CREATE TABLE users (
    id          VARCHAR(36)  NOT NULL,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(120) NOT NULL,
    password    VARCHAR(128) NOT NULL,
    is_admin    BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  DATETIME     NOT NULL,
    updated_at  DATETIME     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
);

-- --------------------------------------------------------- AMENITIES
CREATE TABLE amenities (
    id          VARCHAR(36) NOT NULL,
    name        VARCHAR(50) NOT NULL,
    created_at  DATETIME    NOT NULL,
    updated_at  DATETIME    NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- ------------------------------------------------------------ PLACES
CREATE TABLE places (
    id          VARCHAR(36)   NOT NULL,
    title       VARCHAR(100)  NOT NULL,
    description TEXT,
    price       DECIMAL(10,2) NOT NULL,
    latitude    FLOAT         NOT NULL,
    longitude   FLOAT         NOT NULL,
    owner_id    VARCHAR(36)   NOT NULL,
    created_at  DATETIME      NOT NULL,
    updated_at  DATETIME      NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_places_owner
        FOREIGN KEY (owner_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ----------------------------------------------------------- REVIEWS
CREATE TABLE reviews (
    id          VARCHAR(36) NOT NULL,
    text        TEXT        NOT NULL,
    rating      INT         NOT NULL,
    user_id     VARCHAR(36) NOT NULL,
    place_id    VARCHAR(36) NOT NULL,
    created_at  DATETIME    NOT NULL,
    updated_at  DATETIME    NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT chk_rating CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT unique_user_place_review UNIQUE (user_id, place_id),
    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_place
        FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);

-- ---------------------------------------- PLACE_AMENITY (many-to-many)
CREATE TABLE place_amenity (
    place_id    VARCHAR(36) NOT NULL,
    amenity_id  VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    CONSTRAINT fk_pa_place
        FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    CONSTRAINT fk_pa_amenity
        FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);
