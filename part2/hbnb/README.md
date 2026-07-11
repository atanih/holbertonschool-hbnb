# HBnB Evolution - Part 2: Business Logic Layer

## Overview
This directory contains the core business logic layer of the HBnB application, implementing the entity classes and their relationships as designed in Part 1.

## Core Models

### BaseModel
The foundation class for all entities. Provides:
- **UUID Generation**: Unique identifier (`id`) for each object
- **Timestamps**: `created_at` and `updated_at` for lifecycle tracking
- **Methods**:
  - `save()`: Updates the `updated_at` timestamp
  - `update(data)`: Updates object attributes from a dictionary

### User
Represents a user in the system.
- **Attributes**: `first_name`, `last_name`, `email`, `is_admin`, `id`, `created_at`, `updated_at`
- **Validation**: Email format, name length (max 50 chars)
- **Default**: `is_admin = False`

### Place
Represents a rental property.
- **Attributes**: `title`, `description`, `price`, `latitude`, `longitude`, `owner`, `reviews`, `amenities`, `id`, `created_at`, `updated_at`
- **Validation**: Price > 0, latitude [-90, 90], longitude [-180, 180]
- **Methods**:
  - `add_review(review)`: Associates a review with the place
  - `add_amenity(amenity)`: Associates an amenity with the place

### Review
Represents a user review for a place.
- **Attributes**: `text`, `rating`, `place`, `user`, `id`, `created_at`, `updated_at`
- **Validation**: Rating between 1 and 5

### Amenity
Represents an amenity offered by a place (e.g., Wi-Fi, Pool).
- **Attributes**: `name`, `id`, `created_at`, `updated_at`
- **Validation**: Name length (max 50 chars)

## Relationships

### User → Place (One-to-Many)
A user can own multiple places. Each place has an `owner` attribute referencing the User.

### Place → Review (One-to-Many)
A place can have multiple reviews. Reviews are stored in the `reviews` list.

### Place ← User (Through Review)
Users can write reviews for places.

### Place → Amenity (Many-to-Many)
A place can have multiple amenities. Amenities are stored in the `amenities` list.

## Running Tests

To verify the implementation, run the test suite:

```bash
python3 app/models/tests.py
```

Expected output:

User creation test passed!
Place creation and relationship test passed!
Amenity creation test passed!

## File Structure

app/models/
├── init.py           # Exports all models
├── base_model.py         # BaseModel class
├── user.py               # User class
├── place.py              # Place class
├── review.py             # Review class
├── amenity.py            # Amenity class
└── tests.py              # Test suite

## Key Design Principles

- **DRY (Don't Repeat Yourself)**: Common attributes in BaseModel
- **Validation**: Input validation in `__init__` methods
- **Fail Fast**: Raise errors immediately on invalid data
- **Relationships**: Properly maintained between entities
- **UUID Security**: Non-sequential identifiers for security

## Next Steps

The next phase will implement the API endpoints (Task 2) to expose these models through Flask-RESTx endpoints.