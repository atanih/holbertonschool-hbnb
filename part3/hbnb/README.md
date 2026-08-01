# HBnB — Part 3: Enhanced Backend with Authentication and Database Integration

Backend de HBnB con autenticación JWT, control de acceso por roles (RBAC) y
persistencia real mediante SQLAlchemy (SQLite en desarrollo, MySQL en producción).

## Estructura

```
part3/
├── app/
│   ├── __init__.py           # Application Factory + extensiones
│   ├── api/v1/               # auth, users, places, reviews, amenities
│   ├── models/               # BaseModel, User, Place, Review, Amenity, associations
│   ├── persistence/          # Repository, SQLAlchemyRepository y repos por entidad
│   └── services/             # HBnBFacade (singleton `facade`)
├── sql/                      # schema.sql, initial_data.sql, test_crud.sql, er_diagram.mmd
├── tests/                    # tests de flujo de autenticación
├── config.py                 # Development / Production / Testing
└── run.py
```

## Instalación

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

export SECRET_KEY=$(python3 -c "import secrets;print(secrets.token_hex(32))")
export JWT_SECRET_KEY=$(python3 -c "import secrets;print(secrets.token_hex(32))")

python3 run.py          # crea las tablas y arranca en http://127.0.0.1:5000
```

Documentación interactiva (Swagger): <http://127.0.0.1:5000/api/v1/>

## Crear el usuario administrador

```bash
sqlite3 instance/development.db < sql/initial_data.sql
# admin@hbnb.io / admin1234
```

## Endpoints

| Método | Ruta | Acceso |
|---|---|---|
| POST | `/api/v1/auth/login` | Público |
| GET | `/api/v1/auth/protected` | Autenticado |
| POST | `/api/v1/users/` | **Admin** |
| GET | `/api/v1/users/`, `/api/v1/users/<id>` | Público |
| PUT | `/api/v1/users/<id>` | Uno mismo (sin email/password) · Admin (todo) |
| GET | `/api/v1/amenities/`, `/api/v1/amenities/<id>` | Público |
| POST / PUT | `/api/v1/amenities/`, `/api/v1/amenities/<id>` | **Admin** |
| GET | `/api/v1/places/`, `/api/v1/places/<id>`, `/api/v1/places/<id>/reviews` | Público |
| POST | `/api/v1/places/` | Autenticado |
| PUT / DELETE | `/api/v1/places/<id>` | Dueño o Admin |
| GET | `/api/v1/reviews/`, `/api/v1/reviews/<id>` | Público |
| POST | `/api/v1/reviews/` | Autenticado (no tu place, 1 por place) |
| PUT / DELETE | `/api/v1/reviews/<id>` | Autor o Admin |

## Diagrama ER

```mermaid
erDiagram
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "receives"
    PLACE }o--o{ AMENITY : "has"

    USER {
        string id PK "UUID4"
        string first_name
        string last_name
        string email UK
        string password "bcrypt hash"
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACE {
        string id PK "UUID4"
        string title
        text description
        decimal price
        float latitude
        float longitude
        string owner_id FK "users.id"
        datetime created_at
        datetime updated_at
    }

    REVIEW {
        string id PK "UUID4"
        text text
        int rating "1-5"
        string user_id FK "users.id"
        string place_id FK "places.id"
        datetime created_at
        datetime updated_at
    }

    AMENITY {
        string id PK "UUID4"
        string name UK
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        string place_id PK_FK "places.id"
        string amenity_id PK_FK "amenities.id"
    }
```

## Tests

```bash
python3 -m unittest discover tests -v
python3 -m flake8 app/ config.py run.py
```

## Autor

- Antonio J. Torres Alvarado
