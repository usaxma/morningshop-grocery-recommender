# MorningShop — Grocery Store Recommender

Django grocery storefront with **item-based collaborative filtering**. Shoppers browse products, add them to a session cart, check out, rate items, and get similar-product suggestions from a user–item rating matrix.

## What it is

| Piece | Role |
|---|---|
| `shop` | Catalog, product pages, cart, checkout, search |
| `recommender` | Pearson correlation on `datasets/ratings.csv` + `datasets/products.csv` |
| `user_control` | Customer accounts, ratings, orders, admin dashboard |
| `upload_media` | Product images |

Recommendations are exposed as JSON:

- `GET /api/gen_recommendations/<product_id>`
- `GET /api/get_product_by_id/<product_id>`

The storefront uses those endpoints on the product page to show similar groceries.

## Stack

- Django 3.x
- Pandas / NumPy (item–item correlation)
- SQLite by default (MySQL optional)
- Session cart (signed cookies)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

To use MySQL instead of SQLite, set `USE_SQLITE=False` in `.env` and fill in `DB_*`.

## Project layout

```
morningshop-grocery-recommender/
├── manage.py
├── morningshop/          # Django project settings & URLs
├── shop/                 # Storefront, cart, checkout
├── recommender/          # Collaborative filtering API
├── user_control/         # Auth, profiles, admin
├── datasets/             # products.csv, ratings.csv
└── upload_media/         # Product photos
```

## Recommender

1. Merge product titles with user ratings  
2. Build a user × product rating pivot  
3. Correlate the selected product’s rating vector with every other product  
4. Return the top items with correlation > 0.4  

## Notes

- Copy `.env.example` to `.env`. Do not commit secrets.  
- Static CSS/JS live under `shop/static/`.  
- Admin: `/admin/` after `python manage.py createsuperuser`.
