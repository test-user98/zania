# E-commerce Backend API

A FastAPI-based e-commerce backend with PostgreSQL database, running in Docker containers.

## Features

- Product management (create/list)
- Order processing with stock validation
- Order status updates
- PostgreSQL database
- Docker containerization
- Automated testing

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Pytest

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-backend
```

2. Start the application:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Products

- `GET /products/`: List all products
- `POST /products/`: Create a product
```json
{
    "name": "Product Name",
    "description": "Product Description",
    "price": 99.99,
    "stock": 100
}
```

### Orders

- `GET /orders/`: List all orders
- `POST /orders/`: Create an order
```json
{
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
}
```
- `PUT /orders/{order_id}/`: Update order status
```json
{
    "status": "shipped"
}
```

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
docker-compose run test_runner
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── api.py         # FastAPI routes
│   ├── crud.py        # Database operations
│   ├── models.py      # SQLAlchemy models
│   └── schemas.py     # Pydantic models
├── tests/
│   └── test_api.py    # API tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Configuration

Environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `TEST_DATABASE_URL`: Test database connection string

## License

MIT License
