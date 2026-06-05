# HBnB Evolution - Technical Documentation

## Introduction
This document serves as the technical blueprint 
for the HBnB Evolution application, a simplified 
AirBnB-like platform. It includes the architecture 
design, business logic, and API interaction flows 
that will guide the implementation phases.

---

## 1. High-Level Architecture

### Overview
The application follows a three-layer architecture
communicating via the Facade Pattern.

### Diagram

```mermaid
classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
        +UserService
        +PlaceService
        +ReviewService
        +AmenityService
    }
    class BusinessLogicLayer {
        +User
        +Place
        +Review
        +Amenity
    }
    class PersistenceLayer {
        +DatabaseAccess
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
    }
    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
```

### Explanation
- *Presentation Layer:* Handles user interaction via services and APIs.
- *Business Logic Layer:* Contains core models and business rules.
- *Persistence Layer:* Manages data storage and retrieval.
- *Facade Pattern:* Simplifies communication between layers.

---

## 2. Business Logic Layer

### Overview
Contains the four core entities of the application.

### Diagram

```mermaid
classDiagram
    direction LR
    class User {
        +UUID id
        +String first_name
        +String last_name
        +String email
        -String password
        +Boolean is_admin
        +DateTime created_at
        +DateTime updated_at
        +register()
        +update_profile()
        +delete()
    }
    class Place {
        +UUID id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +DateTime created_at
        +DateTime updated_at
        +create()
        +update()
        +delete()
        +list()
    }
    class Review {
        +UUID id
        +Int rating
        +String comment
        +DateTime created_at
        +DateTime updated_at
        +create()
        +update()
        +delete()
        +list_by_place()
    }
    class Amenity {
        +UUID id
        +String name
        +String description
        +DateTime created_at
        +DateTime updated_at
        +create()
        +update()
        +delete()
        +list()
    }
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" *-- "0..*" Review : has
    Place "0..*" *-- "0..*" Amenity : includes
```

### Explanation
- *User:* Application user, can be regular or admin.
- *Place:* Property listed by a user, includes location and price.
- *Review:* Review left by a user for a place.
- *Amenity:* Feature associated with a place.

---

## 3. API Interaction Flow

### 3.1 User Registration

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: POST /users (I want to join)
    API->>BusinessLogic: check_if_user_is_new()
    BusinessLogic->>Database: search_email()
    Database-->>BusinessLogic: email_available
    BusinessLogic->>Database: save_new_user()
    Database-->>BusinessLogic: user_ready
    BusinessLogic-->>API: registration_done
    API-->>User: 201 Created
```

### 3.2 Place Creation

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: POST /places (here is my place!)
    API->>BusinessLogic: validate_place_info()
    BusinessLogic->>Database: store_place()
    Database-->>BusinessLogic: place_stored
    BusinessLogic-->>API: place_is_live
    API-->>User: 201 Created
```

### 3.3 Review Submission

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: POST /reviews (rating, comment)
    API->>BusinessLogic: validate_review()
    BusinessLogic->>Database: save_review()
    Database-->>BusinessLogic: review_saved
    BusinessLogic-->>API: review_published
    API-->>User: 201 Created
```

### 3.4 Fetching a List of Places

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: GET /places (show me everything!)
    API->>BusinessLogic: get_all_places()
    BusinessLogic->>Database: fetch_places()
    Database-->>BusinessLogic: here_is_the_data
    BusinessLogic-->>API: places_ready
    API-->>User: 200 OK
```