from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database path
DB_PATH = '/data/products.db'

def init_db():
    """Initialize database with schema"""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_products_table = """
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
    """
    
    cursor.execute(create_products_table)
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Product Service is running'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title as name, description, vendor, product_type, 
               tags, inventory_quantity, price, image_url, code, slug
        FROM jewelry
        WHERE inventory_quantity > 0
    """)
    
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'results': products,
        'success': True
    }), 200

@app.route('/api/product/<slug>', methods=['GET'])
def get_product(slug):
    """Get single product by slug"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title as name, description, vendor, product_type,
               tags, inventory_quantity, price, image_url, code, slug
        FROM jewelry
        WHERE slug = ?
    """, (slug,))
    
    product = cursor.fetchone()
    conn.close()
    
    if product:
        return jsonify({
            'result': dict(product),
            'success': True
        }), 200
    
    return jsonify({'success': False, 'message': 'Product not found'}), 404

if __name__ == '__main__':
    print("Product Service starting on 0.0.0.0:5010")
    app.run(
        host='0.0.0.0', 
        port=5010, 
        debug=True
    )
