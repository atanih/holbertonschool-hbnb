    # Sequence Diagrams - API Calls 

## 1. User Registration

```mermaid

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User-->>API: POST /users (I want to join)
    API-->>BusinessLogic: check_if_user_is_new() 
    BusinessLogic-->>Database: search_email()
    Database-->>BusinessLogic: email_available
    BusinessLogic-->>Database: save_new_user()
    Database-->>BusinessLogic: user_ready
    BusinessLogic-->>API: registration_done
    API-->>User: 201 Created
```

## 2. Place Creation
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

## 3. Review Submission
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

## 4. Fetching a List of Places
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
