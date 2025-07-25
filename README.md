# PaymentSystem

Simple Django + Stripe integration for selling Items and Orders with Discounts and Taxes.

## Quick Start

### Prerequisites

- Docker & Docker Compose (optional for Docker setup)
- Stripe account with API keys

### Setup

1. Clone the repo:

```
git clone <repo-url>
cd PaymentSystem
cp .env.example .env
```

2. Build and start containers:
```
docker-compose build
docker-compose up
```
3. In another terminal, run migrations and create superuser:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```