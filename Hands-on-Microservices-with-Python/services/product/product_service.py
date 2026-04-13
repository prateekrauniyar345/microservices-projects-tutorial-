from flask import Flask, jsonify, request
import sqlite3
import os


"""
Products Table Schema:

Column          | Type    | Nullable | Constraints
-----------------------------------------------------
Code            | INTEGER | NO       | PRIMARY KEY
Title           | TEXT    | YES      | NO
Description     | TEXT    | YES      | NO
Vendor          | TEXT    | YES      | NO
Product         | TEXT    | YES      | NO
Tags            | TEXT    | YES      | NO
Inventory       | REAL    | YES      | NO
Price           | REAL    | YES      | NO
Image           | TEXT    | YES      | NO
"""

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
    CREATE TABLE IF NOT EXISTS products (
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
    """
    
    try:
        cursor.execute(create_products_table)
        conn.commit()
        print("Products table created successfully", flush=True)
    except sqlite3.OperationalError as e:
        print(f"Database error (may be expected if table exists): {e}", flush=True)
        conn.rollback()
    finally:
        conn.close()

# Initialize database on startup
init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Product Service is running'}), 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'product',
        'version': '1.0.0'
    }), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT Code, Title, Description, Vendor, Product, 
               Tags, Inventory, Price, Image
        FROM products
        WHERE Inventory > 0
    """)
    
    products = [dict(row) for row in cursor.fetchall()]
    print("fetched products are : ", products, flush=True)
    conn.close()
    
    return jsonify({
        'results': products,
        'success': True
    }), 200

@app.route('/api/product/<int:code>', methods=['GET'])
def get_product(code):
    """Get single product by code"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT Code, Title, Description, Vendor, Product,
               Tags, Inventory, Price, Image
        FROM products
        WHERE Code = ?
    """, (code,))
    
    product = cursor.fetchone()
    conn.close()
    
    if product:
        return jsonify({
            'result': dict(product),
            'success': True
        }), 200
    
    return jsonify({'success': False, 'message': 'Product not found'}), 404

@app.route('/api/product/create', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.form
        code = data.get('code')
        title = data.get('title')
        description = data.get('description', '')
        vendor = data.get('vendor', '')
        product = data.get('product', '')
        tags = data.get('tags', '')
        inventory = data.get('inventory', 0)
        price = data.get('price', 0)
        image = data.get('image', '')
        
        # Validate required fields
        if not code or not title:
            return jsonify({
                'success': False,
                'message': 'Code and Title are required'
            }), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO products (Code, Title, Description, Vendor, Product, Tags, Inventory, Price, Image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, title, description, vendor, product, tags, inventory, price, image))
            
            conn.commit()
            print(f"✓ Product '{title}' created with code {code}", flush=True)
            
            return jsonify({
                'success': True,
                'message': f'Product {title} created successfully',
                'result': {
                    'Code': code,
                    'Title': title,
                    'Description': description,
                    'Vendor': vendor,
                    'Product': product,
                    'Tags': tags,
                    'Inventory': inventory,
                    'Price': price,
                    'Image': image
                }
            }), 201
        
        except sqlite3.IntegrityError as e:
            conn.rollback()
            print(f"[ERROR] Product creation failed: {str(e)}", flush=True)
            return jsonify({
                'success': False,
                'message': f'Product with code {code} already exists'
            }), 409
        finally:
            conn.close()
    
    except Exception as e:
        print(f"[ERROR] Create product failed: {str(e)}", flush=True)
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("Product Service starting on 0.0.0.0:5010", flush=True)
    app.run(
        host='0.0.0.0', 
        port=5010, 
        debug=True
    )
