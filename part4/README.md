# HBnB — Part 4: Simple Web Client

Front-end en HTML5, CSS3 y JavaScript ES6 que consume la API REST
desarrollada en la Part 3.

## Estructura

```
part4/
├── index.html        # Lista de places + filtro de precio (Task 2)
├── login.html        # Formulario de login (Task 1)
├── place.html        # Detalle de un place + reviews (Task 3)
├── add_review.html   # Formulario de review (Task 4)
├── styles.css        # Estilos de las cuatro páginas (Task 0)
├── scripts.js        # Lógica: fetch, cookies, filtros, formularios
└── images/
    ├── logo.png
    └── icon.png      # favicon
```

## Requisitos previos

La API de la Part 3 debe estar corriendo en `http://127.0.0.1:5000`
y tener CORS habilitado:

```bash
cd ../part3/hbnb
pip install flask-cors
python3 run.py
```

## Cómo ejecutarlo

Sirve los archivos por HTTP (no abras los `.html` con doble clic:
`file://` bloquea las peticiones fetch):

```bash
cd part4
python3 -m http.server 8000
```

Abre <http://localhost:8000/index.html>.

Credenciales del administrador sembrado en `sql/initial_data.sql`:

- Email: `admin@hbnb.io`
- Password: `admin1234`

## Tasks implementadas

| Task | Descripción | Dónde |
|---|---|---|
| 0 · Design | Cuatro páginas con header, nav, footer y estilos | `*.html`, `styles.css` |
| 1 · Login | POST a `/auth/login`, JWT guardado en cookie `token` | `login.html`, `loginUser()` |
| 2 · Index | Fetch de places, filtro de precio en cliente, login link condicional | `index.html`, `fetchPlaces()`, `filterPlacesByPrice()` |
| 3 · Place details | Place por id de la query string, amenities y reviews | `place.html`, `fetchPlaceDetails()` |
| 4 · Add review | POST a `/reviews/`, redirige si no hay sesión | `add_review.html`, `submitReview()` |

## Parámetros fijos del diseño

Las tarjetas de place y de review usan, según especificación:
margen `20px`, padding `10px`, borde `1px solid #ddd` y
radio de borde `10px`.

## Autor

- Antonio J. Torres Alvarado
