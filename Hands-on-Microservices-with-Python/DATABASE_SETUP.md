# SQLite3 Database Setup Guide

This document explains how to set up the SQLite3 databases for the microservices.

## Database Structure

The project uses three separate SQLite3 databases:

### 1. User Database (`data/user.db`)
Stores user account information

**Table: `users`**
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT) - Unique user identifier
- `username` (TEXT UNIQUE) - Username for login
- `email` (TEXT UNIQUE) - User email address
- `password` (TEXT) - Hashed password
- `first_name` (TEXT) - User's first name
- `last_name` (TEXT) - User's last name
- `created_at` (TIMESTAMP) - Account creation timestamp

### 2. Products Database (`data/products.db`)
Stores product catalog information

**Table: `jewelry`**
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT) - Unique product identifier
- `title` (TEXT) - Product name
- `description` (TEXT) - Product description
- `vendor` (TEXT) - Vendor name
- `product_type` (TEXT) - Type of product
- `tags` (TEXT) - Comma-separated tags
- `inventory_quantity` (REAL) - Available stock quantity
- `price` (REAL) - Product price
- `image_url` (TEXT) - URL to product image
- `code` (INTEGER) - Product code
- `slug` (TEXT UNIQUE) - URL-friendly product identifier

### 3. Orders Database (`data/orders.db`)
Stores order and order item information

**Table: `orders`**
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT) - Unique order identifier
- `user_id` (INTEGER) - Reference to user
- `order_date` (TIMESTAMP) - When order was created
- `total_amount` (REAL) - Total order amount
- `status` (TEXT) - Order status (pending, completed, cancelled, etc.)

**Table: `order_items`**
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT) - Unique item identifier
- `order_id` (INTEGER) - Reference to order
- `product_id` (INTEGER) - Reference to product
- `quantity` (INTEGER) - Quantity ordered
- `unit_price` (REAL) - Price at time of order

## Setup Instructions

### Option 1: Automatic Setup (Recommended)

Run the initialization script to automatically create and populate the databases:

```bash
cd /Volumes/ORICO/learnings/microservices/Hands-on-Microservices-with-Python
python3 init_databases.py
```

This will:
- Create the `data/` directory (if it doesn't exist)
- Create all three databases with proper schema
- Populate sample data:
  - **Sample User**: `john` / `password123`
  - **Sample Products**: Laptop, Mouse, Keyboard

### Option 2: Manual Setup

If you prefer to set up databases manually, follow the SQL statements in the schema sections above.

## Using with Docker

The databases are mounted as volumes in `docker-compose.yml`:

```yaml
volumes:
  - ./data:/data
```

This makes the `data/` directory available to all services at `/data/` inside the containers.

## Sample User Account

After running `init_databases.py`, you can log in with:

- **Username**: `john`
- **Password**: `password123`

## Adding More Data

You can add users, products, and orders using any SQLite3 client:

### Add a new user:
```sql
INSERT INTO users (username, email, password, first_name, last_name)
VALUES ('alice', 'alice@example.com', 'secure_password', 'Alice', 'Smith');
```

### Add a new product:
```sql
INSERT INTO jewelry (title, description, vendor, product_type, tags, inventory_quantity, price, image_url, code, slug)
VALUES ('Gold Ring', 'Beautiful gold ring', 'Luxury Jewelry', 'Jewelry', 'ring,gold', 20.0, 599.99, 'ring.jpg', 2001, 'gold-ring');
```

## Troubleshooting

### Databases not found in Docker
Make sure the `data/` folder is mounted correctly:
```bash
docker-compose logs user  # Check if databases are being created
```

### Permission errors
If you get permission errors, ensure the `data/` directory has correct permissions:
```bash
chmod 755 /Volumes/ORICO/learnings/microservices/Hands-on-Microservices-with-Python/data
```

### Reinitialize databases
To start fresh, delete the database files and run `init_databases.py` again:
```bash
rm -f data/*.db
python3 init_databases.py
```
