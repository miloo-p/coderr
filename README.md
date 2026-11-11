# Coderr Backend

REST API for Coderr, a freelancer marketplace where business users offer services and customers order and review them.
Built with Django and Django REST Framework, token authentication and SQLite.

## Requirements

- Python 3.12 or newer
- Git

## Installation

1. Clone the repository and open the folder:

   ```bash
   git clone https://github.com/miloo-p/coderr.git
   cd coderr
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the `.env` file from the example:

   Windows:

   ```bash
   copy .env.example .env
   ```

   macOS / Linux:

   ```bash
   cp .env.example .env
   ```

   Generate a secret key:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Open `.env` and paste the key behind `SECRET_KEY=`.

5. Create the database:

   ```bash
   python manage.py migrate
   ```

6. Optional: create an admin user (needed to delete orders and to use `/admin/`):

   ```bash
   python manage.py createsuperuser
   ```

7. Start the server:

   ```bash
   python manage.py runserver
   ```

   The API is now available at `http://127.0.0.1:8000/api/`.

## Running the tests

```bash
python manage.py test
```

## Notes

- Authentication uses tokens. Send them as `Authorization: Token <token>`.
- Only admin users (staff) can delete orders. Create one with `python manage.py createsuperuser`.
- `GET /api/offers/` and `GET /api/base-info/` work without login, registration and login of course as well.
  All other endpoints need a token.
- `average_rating` in `/api/base-info/` is `0` as long as there are no reviews.
- A second review of the same business user by the same customer returns `400 Bad Request`
  (the documentation names both 400 and 403).
- The `url` of offer details is an absolute URL in the offer list and in the single offer.
- Images (`file` in profiles, `image` in offers) are uploaded as `multipart/form-data`.
- Uploaded files are stored in `media/`, which is not part of the repository.

## Endpoints

| Method             | URL                                              | Description                                             |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------- |
| POST               | `/api/registration/`                             | Register a customer or business user                    |
| POST               | `/api/login/`                                    | Log in and get a token                                  |
| GET, PATCH         | `/api/profile/{pk}/`                             | Read or update a profile                                |
| GET                | `/api/profiles/business/`                        | List all business profiles                              |
| GET                | `/api/profiles/customer/`                        | List all customer profiles                              |
| GET, POST          | `/api/offers/`                                   | List (filter, search, order, paginate) or create offers |
| GET, PATCH, DELETE | `/api/offers/{id}/`                              | Read, update or delete an offer                         |
| GET                | `/api/offerdetails/{id}/`                        | Read a single offer package                             |
| GET, POST          | `/api/orders/`                                   | List own orders or create an order                      |
| PATCH, DELETE      | `/api/orders/{id}/`                              | Update the order status or delete an order (admin only) |
| GET                | `/api/order-count/{business_user_id}/`           | Count running orders of a business user                 |
| GET                | `/api/completed-order-count/{business_user_id}/` | Count completed orders of a business user               |
| GET, POST          | `/api/reviews/`                                  | List (filter, order) or create reviews                  |
| PATCH, DELETE      | `/api/reviews/{id}/`                             | Update or delete an own review                          |
| GET                | `/api/base-info/`                                | Platform statistics                                     |
