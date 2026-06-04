# HBnB Evolution - Technical Documentation

## Description
Simplified AirBnB-like application with a 
three-layer architecture.

## High-Level Package Diagram

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
