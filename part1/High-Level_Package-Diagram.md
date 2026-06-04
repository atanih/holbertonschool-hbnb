# High-Level Package Diagram

## Objective
Illustrates the three-layer architecture of the HBnB 
application and the communication between these layers 
via the facade pattern.

## Diagram

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
    