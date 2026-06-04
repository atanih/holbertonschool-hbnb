# Detailed Class Diagram - Business Logic Layer

## Diagram

mermaid
classDiagram
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
## Entity Descriptions

- **User:** Application user, can be regular or admin.

- **Place:** Property listed by a user, 
includes location and price.

- **Review:** Review left by a user for a place,
includes rating and comment.

- **Amenity:** Feature that can be associated 
with a place.

## Relationships

- **User** owns many **Places**
- **User** writes many **Reviews**
- **Place** has many **Reviews**
- **Place** includes many **Amenities**
