/* ==========================================================
   HBnB - Part 4 : Simple Web Client
   Handles login, list of places, place details and add review.
   ========================================================== */

const API_URL = 'http://127.0.0.1:5000/api/v1';

/* ---------------------------------------------------- COOKIES */

/**
 * Return the value of a cookie by its name, or null if missing.
 */
function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (let i = 0; i < cookies.length; i++) {
        const pair = cookies[i].trim();
        if (pair.startsWith(name + '=')) {
            return decodeURIComponent(pair.substring(name.length + 1));
        }
    }
    return null;
}

function setCookie(name, value) {
    document.cookie = `${name}=${value}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
}

/* ------------------------------------------------------ HELPERS */

/**
 * Read the place id from the query string (?id=<uuid>).
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function showMessage(elementId, text, type) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = text;
    el.className = 'message ' + type;
}

/**
 * Toggle the Login / Logout links depending on the token.
 */
function updateNav(token) {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    if (loginLink) loginLink.style.display = token ? 'none' : 'inline-block';
    if (logoutLink) logoutLink.style.display = token ? 'inline-block' : 'none';
}

/* -------------------------------------------------- TASK 1: LOGIN */

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        setCookie('token', data.access_token);
        window.location.href = 'index.html';
    } else {
        let detail = response.statusText;
        try {
            const err = await response.json();
            detail = err.error || err.msg || detail;
        } catch (e) { /* body was not JSON */ }
        showMessage('login-message', 'Login failed: ' + detail, 'error');
    }
}

/* --------------------------------------------------- TASK 2: INDEX */

let allPlaces = [];

async function fetchPlaces(token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers.Authorization = `Bearer ${token}`;

    const response = await fetch(`${API_URL}/places/`, { headers });
    if (!response.ok) {
        document.getElementById('places-list').innerHTML =
            '<p>Could not load places. Is the API running?</p>';
        return;
    }
    allPlaces = await response.json();
    displayPlaces(allPlaces);
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    list.innerHTML = '';

    if (!places.length) {
        list.innerHTML = '<p>No places available yet.</p>';
        return;
    }

    places.forEach((place) => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.innerHTML =
            `<h2>${place.title}</h2>` +
            `<p class="price">$${place.price} per night</p>` +
            `<a href="place.html?id=${place.id}" class="details-button">` +
            'View Details</a>';
        list.appendChild(card);
    });
}

function filterPlacesByPrice(value) {
    const cards = document.querySelectorAll('.place-card');
    cards.forEach((card) => {
        const price = parseFloat(card.dataset.price);
        const show = value === 'all' || price <= parseFloat(value);
        card.style.display = show ? 'block' : 'none';
    });
}

/* -------------------------------------------- TASK 3: PLACE DETAILS */

async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers.Authorization = `Bearer ${token}`;

    const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
    if (!response.ok) {
        document.getElementById('place-details').innerHTML =
            '<p>Place not found.</p>';
        return;
    }
    const place = await response.json();
    displayPlaceDetails(place);
    displayReviews(place.reviews || []);
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    section.innerHTML = '';

    const host = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : 'Unknown';

    const amenities = (place.amenities || [])
        .map((a) => `<li>${a.name}</li>`)
        .join('');

    section.innerHTML =
        `<h1>${place.title}</h1>` +
        '<div class="place-info">' +
        `<p><strong>Host:</strong> ${host}</p>` +
        `<p><strong>Price per night:</strong> $${place.price}</p>` +
        `<p><strong>Description:</strong> ${place.description || '-'}</p>` +
        '<p><strong>Amenities:</strong></p>' +
        `<ul class="amenity-list">${amenities || '<li>None</li>'}</ul>` +
        '</div>';
}

async function displayReviews(reviews) {
    const section = document.getElementById('reviews');
    section.innerHTML = '';

    if (!reviews.length) {
        section.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    // Map user ids to names so each review can show its author.
    let users = [];
    try {
        const res = await fetch(`${API_URL}/users/`);
        if (res.ok) users = await res.json();
    } catch (e) { /* keep going without names */ }

    const names = {};
    users.forEach((u) => {
        names[u.id] = `${u.first_name} ${u.last_name}`;
    });

    reviews.forEach((review) => {
        const card = document.createElement('article');
        card.className = 'review-card';
        card.innerHTML =
            `<p class="author">${names[review.user_id] || 'Anonymous'}</p>` +
            `<p class="rating">Rating: ${'*'.repeat(review.rating)} ` +
            `(${review.rating}/5)</p>` +
            `<p class="comment">${review.text}</p>`;
        section.appendChild(card);
    });
}

/* ---------------------------------------------- TASK 4: ADD REVIEW */

async function submitReview(token, placeId, reviewText, rating) {
    const response = await fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating, 10),
            place_id: placeId
        })
    });
    return response;
}

async function handleReviewResponse(response, form) {
    if (response.ok) {
        showMessage('review-message', 'Review submitted successfully!',
            'success');
        form.reset();
    } else {
        let detail = response.statusText;
        try {
            const err = await response.json();
            detail = err.error || err.msg || detail;
        } catch (e) { /* body was not JSON */ }
        showMessage('review-message', 'Failed to submit review: ' + detail,
            'error');
    }
}

/* ------------------------------------------------------- BOOTSTRAP */

document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const page = window.location.pathname.split('/').pop() || 'index.html';

    updateNav(token);

    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            deleteCookie('token');
            window.location.href = 'index.html';
        });
    }

    /* ---------------- login.html ---------------- */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    /* ---------------- index.html ---------------- */
    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces(token);
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                filterPlacesByPrice(event.target.value);
            });
        }
    }

    /* ---------------- place.html ---------------- */
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            placeDetails.innerHTML = '<p>No place selected.</p>';
            return;
        }
        fetchPlaceDetails(token, placeId);

        const addReview = document.getElementById('add-review');
        if (addReview) {
            addReview.style.display = token ? 'block' : 'none';
        }

        const reviewForm = document.getElementById('review-form');
        if (reviewForm && token) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const text = document.getElementById('review').value;
                const rating = document.getElementById('rating').value;
                const res = await submitReview(token, placeId, text, rating);
                await handleReviewResponse(res, reviewForm);
                if (res.ok) fetchPlaceDetails(token, placeId);
            });
        }
    }

    /* -------------- add_review.html -------------- */
    if (page === 'add_review.html') {
        if (!token) {
            window.location.href = 'index.html';
            return;
        }
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            window.location.href = 'index.html';
            return;
        }
        const nameEl = document.getElementById('place-name');
        fetch(`${API_URL}/places/${placeId}`)
            .then((r) => (r.ok ? r.json() : null))
            .then((p) => {
                if (p && nameEl) nameEl.textContent = `Place: ${p.title}`;
            });

        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const text = document.getElementById('review').value;
                const rating = document.getElementById('rating').value;
                const res = await submitReview(token, placeId, text, rating);
                await handleReviewResponse(res, reviewForm);
            });
        }
    }
});
