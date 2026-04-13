# Hands-on Microservices Project - Comprehensive Notes

## Overview

This is a **hands-on learning project demonstrating Flask-based microservices architecture**. It implements an **e-commerce order management system** with 4 independent services that communicate via HTTP REST APIs.

The project teaches real-world microservices patterns: independent scaling, separate deployments, decoupled databases, and resilient system design.

---

## Repository Structure

```
/Volumes/ORICO/learnings/microservices/
│
├── Hands-on-Microservices-with-Python/     # Main project directory
│   │
│   ├── app/                                 # Frontend Service (Flask web app)
│   │   ├── app.py                          # Flask app initialization & config
│   │   ├── requirements.txt                # Python dependencies
│   │   │
│   │   ├── frontend/                       # Frontend blueprint & routes
│   │   │   ├── __init__.py                # Blueprint creation
│   │   │   ├── routes.py                  # Route handlers (home, login, products, checkout)
│   │   │   ├── forms.py                   # WTForms forms (LoginForm, RegisterForm)
│   │   │   │
│   │   │   ├── api/                       # API Client classes (talk to microservices)
│   │   │   │   ├── UserClient.py         # Calls user service
│   │   │   │   ├── ProductClient.py      # Calls product service
│   │   │   │   └── OrderClient.py        # Calls order service
│   │   │   │
│   │   │   └── templates/                 # Jinja2 HTML templates
│   │   │       ├── base.html              # Base template with Bootstrap
│   │   │       ├── nav_header.html        # Navigation bar
│   │   │       ├── home/
│   │   │       │   └── index.html         # Product listing page
│   │   │       ├── login/
│   │   │       │   └── index.html         # Login form
│   │   │       ├── register/
│   │   │       │   └── index.html         # Registration form
│   │   │       ├── product/
│   │   │       │   └── index.html         # Product detail & add-to-cart
│   │   │       ├── order/
│   │   │       │   └── thankyou.html      # Order confirmation
│   │   │       └── macros/
│   │   │           ├── _macros_form.html  # Form field rendering
│   │   │           └── _macros_basket.html# Cart item counter
│   │   │
│   │   └── static/
│   │       └── css/
│   │           └── main.css               # Basic styling
│   │
│   ├── services/                          # Microservices (run separately)
│   │   ├── Dockerfile.services           # Docker image for all services
│   │   ├── user_service.py               # User authentication service
│   │   ├── product_service.py            # Product catalog service
│   │   └── order_service.py              # Order/cart management service
│   │
│   ├── data/                             # SQLite3 databases (created at runtime)
│   │   ├── user.db                       # User accounts & authentication
│   │   ├── products.db                   # Product catalog
│   │   └── orders.db                     # Orders & shopping carts
│   │
│   ├── tests/
│   │   └── test_pages.py                 # Basic integration tests
│   │
│   ├── Dockerfile                        # Image for frontend service
│   ├── docker-compose.yml                # Local dev setup (all 4 services)
│   ├── docker-compose.deploy.yml         # Production deployment config
│   ├── init_databases.py                 # Script to populate databases
│   │
│   ├── DATABASE_SETUP.md                 # Database schema documentation
│   ├── DOCKER_SETUP.md                   # Docker setup guide
│   └── README.md                         # Project overview
│
├── docs/                                  # Documentation
│   ├── intro.md                          # Microservices concepts
│   ├── Notes.md                          # This file
│   └── getting started for project-Hands-on-Microservices.md
│
└── doc assets/                            # Images & diagrams

```

---

## Microservices Architecture

### Services Overview

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| **Frontend** | 5010 / 8080 | None (session-based) | Web UI, routes, templates |
| **User Service** | 5001 | `user.db` | Registration, login, user profiles |
| **Product Service** | 5002 | `products.db` | Product catalog & inventory |
| **Order Service** | 5003 | `orders.db` | Shopping carts & order management |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND (Port 5010)               │
│            Flask Web App + Jinja2 Templates          │
│                 (routes.py, forms.py)                │
│                                                      │
│  UserClient          ProductClient      OrderClient │
│  (HTTP REST)         (HTTP REST)         (HTTP REST) │
└────────┬─────────────────┬──────────────────┬────────┘
         │                 │                  │
         │                 │                  │
┌────────▼────────┐ ┌──────▼──────────┐ ┌───▼─────────────┐
│  USER SERVICE   │ │ PRODUCT SERVICE │ │ ORDER SERVICE   │
│  (Port 5001)    │ │ (Port 5002)     │ │ (Port 5003)     │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│  /api/user/     │ │ /api/products   │ │ /api/order      │
│  login          │ │ /api/product/:id│ │ /api/order/...  │
│  create         │ │                 │ │ add-item        │
│  exist          │ │                 │ │ update          │
│  get            │ │                 │ │ checkout        │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│                 │ │                 │ │                 │
│   user.db      │ │  products.db   │ │   orders.db     │
│ (SQLite3)      │ │ (SQLite3)      │ │ (SQLite3)       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## How Services Are Developed

### 1. Frontend Service (app/app.py, app/frontend/)

**Purpose**: Main web application that users interact with

**Key Components**:
- `app.py`: Flask initialization, LoginManager setup, blueprint registration
- `frontend/routes.py`: All route handlers
- `frontend/forms.py`: WTForms validation objects
- `frontend/api/`: Client classes for calling other services

**Routes Implemented**:
- `GET /` - Home page, displays all products
- `GET/POST /login` - User login with form validation
- `GET/POST /register` - New user registration
- `GET /logout` - Clear session and redirect
- `GET/POST /product/<code>` - Product detail page, add to cart
- `GET /checkout` - View cart and process checkout
- `GET /order/thank-you` - Order confirmation

**Session Management**:
```python
session['user']          # User object {username, email, first_name, last_name}
session['user_api_key'] # API key for authorization with other services
session['order']        # Current shopping cart {items, total, status}
```

**API Client Pattern** (UserClient, ProductClient, OrderClient):
- All make HTTP requests to microservices
- Use `Authorization: Basic {api_key}` header for authentication
- 5-second timeout with graceful error handling
- Return empty defaults on connection failure

---

### 2. User Service (services/user_service.py)

**Purpose**: Handle user authentication and profiles

**Database** (`data/user.db`):
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**API Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service status check |
| `/api/user/login` | POST | Validate username/password, return API key |
| `/api/user/<username>/exist` | GET | Check if username is taken |
| `/api/user/create` | POST | Create new user account |
| `/api/user` | GET | Get current user (requires auth header) |

**Flow Example** (Login):
```
1. Frontend sends POST /api/user/login with username & password
2. User Service queries database for matching user
3. If password matches, returns: {api_key: 'mock-api-key-12345', user_id: 1}
4. Frontend stores api_key in session
5. All future requests include Authorization header with this key
```

---

### 3. Product Service (services/product_service.py)

**Purpose**: Manage product catalog and inventory

**Database** (`data/products.db`):
```sql
CREATE TABLE products (
    Code INTEGER PRIMARY KEY,
    Title TEXT,
    Description TEXT,
    Vendor TEXT,
    Product TEXT,
    Tags TEXT,
    Inventory REAL,
    Price REAL,
    Image TEXT
);
```

**API Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service status check |
| `/api/products` | GET | List all products with inventory > 0 |
| `/api/product/<code>` | GET | Get single product by code |

**Response Format**:
```json
{
    "results": [
        {
            "Code": 1001,
            "Title": "Laptop Dell",
            "Price": 899.99,
            "Inventory": 10,
            "Image": "laptop.jpg"
        }
    ],
    "success": true
}
```

---

### 4. Order Service (services/order_service.py)

**Purpose**: Manage shopping carts and process orders

**Databases** (`data/orders.db`):
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL DEFAULT 0,
    status TEXT DEFAULT 'pending'  -- pending, completed, cancelled
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

**API Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service status check |
| `/api/order` | GET | Get pending order for authenticated user |
| `/api/order/add-item` | POST | Add product to cart (creates order if needed) |
| `/api/order/update` | POST | Get updated order (for refreshing cart) |
| `/api/order/checkout` | POST | Mark order as completed |

**Authentication**:
- Extracts user_id from Authorization header (simplified for learning)
- All endpoints require: `Authorization: Basic {api_key}`

**Cart Operations Flow**:
```
1. User logs in → gets api_key
2. User clicks "Add to Cart" → POST /api/order/add-item (auth header required)
3. Service creates new order if doesn't exist, adds item
4. Service calculates total_amount = unit_price × quantity
5. Returns updated order with all items
6. Frontend stores in session['order'] and displays
7. User clicks Checkout → POST /api/order/checkout
8. Service updates order status to 'completed'
```

---

## Technology Stack

### Backend
- **Python 3.13-slim** (Docker image)
- **Flask 3.1.3** - Web framework
- **Flask-Login 0.6.3** - Authentication management
- **Flask-WTF 1.2.2** - Form validation & CSRF protection
- **Flask-Bootstrap 3.3.7** - Bootstrap CSS integration
- **Requests 2.32.5** - HTTP client for API calls
- **SQLite3** (built-in) - Database

### Frontend
- **Jinja2 3.1.x** - Template engine
- **Bootstrap 3.3.7** - CSS framework
- **jQuery 1.12.4** - JavaScript utilities
- **WTForms 3.2.1** - Form rendering & validation

### Containerization & Orchestration
- **Docker** - Container images
- **Docker Compose** - Multi-container orchestration

### Development
- **Pytest 8.4.2** - Testing framework
- **Passlib 1.7.4** - Password hashing (available but not used yet)

---

## How Services Communicate

### Request/Response Pattern

**All API requests**:
1. Include Authorization header: `Authorization: Basic {api_key}`
2. Use form-encoded data: `Content-Type: application/x-www-form-urlencoded`
3. Have 5-second timeout for network calls
4. Return JSON responses with `success` flag and `result` data

**Error Handling**:
- Connection errors → return empty default (dict/list)
- Validation errors → return `{success: false, message: '...'}`
- Success responses → return `{success: true, result: {...}}`

**Example**: Frontend adds item to cart
```python
# Frontend (OrderClient.py)
POST http://order:5010/api/order/add-item
Headers: Authorization: Basic {api_key}
Data: product_id=1001&qty=2

# Order Service Response
{
    "result": {
        "id": 5,
        "user_id": 1,
        "items": [
            {"product_id": 1001, "quantity": 2, "unit_price": 899.99}
        ],
        "total": 1799.98,
        "status": "pending"
    },
    "success": true
}

# Frontend stores in session['order']
session['order'] = response['result']
```

---

## Docker Configuration

### Development Setup (docker-compose.yml)

```yaml
services:
  user:          # Port 5001
  product:       # Port 5002
  order:         # Port 5003
  frontend:      # Port 8080
  
network: microservices-network (bridge)
volumes: ./data:/data (for databases)
```

**To run**:
```bash
docker-compose up --build    # Build and start all services
docker-compose down          # Stop all services
```

All services run in the same Docker network so they can communicate using service names.

### Dockerfile for Services

```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN pip install flask flask-login flask-wtf requests passlib
EXPOSE 5010
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5010"]
```

### Dockerfile for Frontend

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
EXPOSE 5010
CMD ["flask", "run", "--host=0.0.0.0", "--port=5010"]
```

---

## Database Schemas

### 1. User Database (data/user.db)
Stores user account credentials and profile info.

**Table: `users`**
- `id` - Auto-incrementing primary key
- `username` - Unique, used for login
- `email` - Unique email address
- `password` - Currently plaintext (should be hashed in production)
- `first_name` / `last_name` - Display name
- `created_at` - Registration timestamp

**Sample Data**:
```
| id | username | email | password | first_name | last_name |
|----|----------|-------|----------|------------|-----------|
| 1  | john     | john@example.com | password123 | John | Doe |
```

### 2. Product Database (data/products.db)
Stores product catalog with pricing and inventory.

**Table: `products`**
- `Code` - Primary key, product ID
- `Title` - Product name
- `Description` - Detailed description
- `Vendor` - Manufacturer
- `Product` - Category/type
- `Tags` - CSV tags (e.g., "electronics,laptop,computer")
- `Inventory` - Stock quantity
- `Price` - Unit price
- `Image` - Image URL or filename

**Sample Data**:
```
| Code | Title | Vendor | Price | Inventory |
|------|-------|--------|-------|-----------|
| 1001 | Laptop Dell | Dell | 899.99 | 10 |
| 1002 | Wireless Mouse | Logitech | 29.99 | 50 |
```

### 3. Order Database (data/orders.db)
Stores shopping carts (pending orders) and completed orders.

**Table: `orders`**
- `id` - Order ID (auto-increment)
- `user_id` - Reference to user
- `order_date` - When order was created
- `total_amount` - Sum of all item prices × quantities
- `status` - 'pending' or 'completed' or 'cancelled'

**Table: `order_items`** (Details of each item in an order)
- `id` - Item ID
- `order_id` - Foreign key to orders table
- `product_id` - Reference to product
- `quantity` - How many units ordered
- `unit_price` - Price at time of order (for historical accuracy)

**Data Example**:
```
orders table:
| id | user_id | order_date | total_amount | status |
|----|---------|----------|--------------|--------|
| 5  | 1       | 2026-04-12 | 1799.98 | pending |

order_items table:
| id | order_id | product_id | quantity | unit_price |
|----|----------|-----------|----------|------------|
| 12 | 5        | 1001      | 2        | 899.99     |
| 13 | 5        | 1002      | 1        | 29.99      |
```

---

## Current State & Completeness

### ✅ Complete/Functional
- Project structure and organization
- Docker containerization (all 4 services work)
- Database schemas (tables created correctly)
- Frontend UI (All pages render with Bootstrap)
- API client classes (talk to services correctly)
- Route handlers (login, register, product pages functional)
- Session management (user/order stored properly)
- Basic error handling with graceful defaults

### ⚠️ Partial/Needs Work
- Password hashing (passlib installed but not used - plaintext passwords)
- Auth token validation (User service returns 'mock-api-key', not validated)
- Database initialization (init_databases.py exists, needs manual run)
- Product seeding (init script has sample data, not auto-loaded)
- Incomplete route in routes.py (checkout doesn't redirect to thank-you)

### ❌ Not Implemented
- Rate limiting on API endpoints
- Logging/monitoring across services
- Error notification/emails
- Payment processing integration
- Inventory decrement on checkout
- Order status notifications
- Admin dashboard
- Production security hardening

---

## Key Design Patterns Used

1. **Service-Oriented Architecture**
   - Each service owns its data
   - Services communicate via REST APIs
   - Decoupled but coordinated

2. **Client Pattern**
   - Frontend has client classes (UserClient, ProductClient, OrderClient)
   - Each client handles one service's communication
   - Encapsulates API details, handles errors

3. **Session-Based State Management**
   - User info stored in Flask session
   - Order/cart stored in Flask session
   - API key used for inter-service auth

4. **Layered Architecture**
   - Routes (frontend/routes.py) - Business logic
   - Forms (frontend/forms.py) - Validation
   - API Clients (frontend/api/) - External communication
   - Templates (frontend/templates/) - Presentation

---

## How to Run Locally

### Prerequisites
- Docker & Docker Compose installed
- `cd` to `Hands-on-Microservices-with-Python/`

### Steps
```bash
# 1. Start all services
docker-compose up --build

# 2. Seed databases with sample data
docker exec frontend python init_databases.py

# 3. Access frontend
open http://localhost:8080

# 4. Login with test user
Username: john
Password: password123
```

### Stopping
```bash
docker-compose down
```

---

## Important Notes for Development

1. **Hardcoded Service URLs**: Services communicate via Docker service names
   - `http://user:5010` not `http://localhost:5001`
   - This only works inside Docker network

2. **API Keys**: Currently just mock strings ("mock-api-key-12345")
   - In production, use JWT tokens with expiration
   - Validate signatures on every request

3. **Databases**: SQLite3 runs in-memory in containers
   - Data persists via volume mount: `./data:/data`
   - Not for production (use PostgreSQL/MySQL)

4. **Error Handling**: Frontends has fallbacks
   - If service unavailable, returns empty cart/product list
   - No user-facing error messages yet
   - Should implement circuit breaker pattern for resilience

5. **Authentication**: Basic auth header (not REST standard)
   - No traditional OAuth/JWT flow
   - Good for learning, not recommended for production
