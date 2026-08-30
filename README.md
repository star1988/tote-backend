# Tote and Trend — Backend API

A REST API for managing products and orders for Tote and Trend, an e-commerce tote bag brand. Built to practice real backend engineering fundamentals: authentication, relational data modeling, business-rule enforcement, automated testing, and cloud deployment.

**Live API:** `https://tote-backend-pgjq.onrender.com/docs`

## Features

- **Product management** — full CRUD (create, read, update, delete) for the product catalog
- **Order processing with real business logic** — orders validate against current stock before confirming, and automatically adjust inventory on order placement or cancellation
- **JWT authentication** — write operations (create/update/delete) are protected; only authenticated requests can modify data
- **Data integrity protection** — products with existing order history can't be deleted, preventing orphaned records
- **Automated tests** — pytest suite covering authentication, authorization, and business logic (stock validation)
- **Interactive API docs** — auto-generated Swagger UI for testing every endpoint directly in the browser

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (hosted on Supabase)
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Auth:** JWT (python-jose) + bcrypt password hashing
- **Testing:** pytest
- **Deployment:** Render

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|--------------|----------------|
| POST | `/login` | Authenticate and receive a JWT token | No |
| GET | `/products/` | List all products | No |
| GET | `/products/{id}` | Get a single product | No |
| POST | `/products/` | Create a new product | Yes |
| PUT | `/products/{id}` | Update a product | Yes |
| DELETE | `/products/{id}` | Delete a product (blocked if it has orders) | Yes |
| GET | `/orders/` | List all orders | No |
| GET | `/orders/{id}` | Get a single order | No |
| POST | `/orders/` | Place an order (validates stock) | Yes |
| DELETE | `/orders/{id}` | Cancel an order (restores stock) | Yes |

## Running Locally

```bash
# Clone the repo
git clone https://github.com/star1988/tote-backend.git
cd tote-backend

# Set up a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create a .env file with:
# DATABASE_URL=your-database-url
# SECRET_KEY=your-secret-key
# ADMIN_PASSWORD=your-admin-password

# Run the server
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Running Tests

```bash
pytest
```

## What This Project Demonstrates

- Designing a relational data model with foreign key relationships
- Enforcing real business rules at the API layer (stock checks, referential integrity)
- Implementing token-based authentication from scratch
- Writing automated tests for both security and business logic
- Debugging and resolving real deployment issues (dependency management, environment configuration, database connection troubleshooting, IPv6/proxy networking constraints)
- Deploying a Python backend to a live, publicly accessible production environment
