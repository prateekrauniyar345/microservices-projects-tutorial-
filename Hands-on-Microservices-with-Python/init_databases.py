#!/usr/bin/env python3
"""
Database initialization script
Creates and populates SQLite3 databases for the microservices
"""

import sqlite3
import os
from pathlib import Path

# Create data directory
data_dir = Path(__file__).parent / 'data'
data_dir.mkdir(exist_ok=True)

# User Database
print("Initializing user database...")
user_db = data_dir / 'user.db'
conn = sqlite3.connect(str(user_db))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,     
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Insert sample user
try:
    cursor.execute("""
    INSERT INTO users (username, email, password, first_name, last_name)
    VALUES (?, ?, ?, ?, ?)
    """, ('john', 'john@example.com', 'password123', 'John', 'Doe'))
    print("✓ Sample user 'john' created")
except sqlite3.IntegrityError:
    print("✓ User already exists")

conn.commit()
conn.close()
print("✓ User database initialized\n")

# Products Database
print("Initializing products database...")
products_db = data_dir / 'products.db'
conn = sqlite3.connect(str(products_db))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jewelry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    vendor TEXT,
    product_type TEXT,
    tags TEXT,
    inventory_quantity REAL,
    price REAL,
    image_url TEXT,
    code INTEGER,
    slug TEXT UNIQUE
);
""")

# Insert sample products
sample_products = [
    ('Laptop Dell', 'High-performance laptop', 'Dell', 'Electronics', 'laptop,computer', 10.0, 899.99, 'laptop.jpg', 1001, 'laptop-dell'),
    ('Wireless Mouse', 'Ergonomic wireless mouse', 'Logitech', 'Electronics', 'mouse,accessory', 50.0, 29.99, 'mouse.jpg', 1002, 'mouse-wireless'),
    ('Mechanical Keyboard', 'RGB mechanical keyboard', 'Corsair', 'Electronics', 'keyboard,gaming', 25.0, 129.99, 'keyboard.jpg', 1003, 'keyboard-mechanical'),
]

for product in sample_products:
    try:
        cursor.execute("""
        INSERT INTO jewelry (title, description, vendor, product_type, tags, inventory_quantity, price, image_url, code, slug)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, product)
        print(f"✓ Product '{product[0]}' created")
    except sqlite3.IntegrityError:
        print(f"✓ Product '{product[0]}' already exists")

conn.commit()
conn.close()
print("✓ Products database initialized\n")

# Orders Database
print("Initializing orders database...")
orders_db = data_dir / 'orders.db'
conn = sqlite3.connect(str(orders_db))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL DEFAULT 0,
    status TEXT DEFAULT 'pending'
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES jewelry(id)
);
""")

conn.commit()
conn.close()
print("✓ Orders database initialized\n")

print("=" * 50)
print("All databases initialized successfully!")
print("=" * 50)
print("\nDatabase paths:")
print(f"  User DB:     {user_db}")
print(f"  Products DB: {products_db}")
print(f"  Orders DB:   {orders_db}")
