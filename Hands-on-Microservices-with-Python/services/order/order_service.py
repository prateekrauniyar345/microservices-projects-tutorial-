from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database path
DB_PATH = '/data/orders.db'

def init_db():
    """Initialize database with schema"""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Orders Table
    create_orders = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount REAL DEFAULT 0,
        status TEXT DEFAULT 'pending'
    );
    """
    
    # Order Items Table
    create_order_items = """
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(code)
    );
    """
    
    cursor.execute(create_orders)
    cursor.execute(create_order_items)
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def get_user_id_from_auth(auth_header):
    """Extract user ID from auth header (simplified)"""
    if auth_header.startswith('Basic '):
        # For now, assume user_id = 1 (in production, decode the token properly)
        return 1
    return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Order Service is running'}), 200

@app.route('/api/order', methods=['GET'])
def get_order():
    """Get current order for user"""
    auth_header = request.headers.get('Authorization', '')
    user_id = get_user_id_from_auth(auth_header)
    
    if not user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get pending order for user
    cursor.execute("""
        SELECT id, user_id, total_amount, status
        FROM orders
        WHERE user_id = ? AND status = 'pending'
        ORDER BY order_date DESC
        LIMIT 1
    """, (user_id,))
    
    order = cursor.fetchone()
    
    if order:
        order_id = order['id']
        # Get order items
        cursor.execute("""
            SELECT id, product_id, quantity, unit_price
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'result': {
                'id': order['id'],
                'user_id': order['user_id'],
                'items': items,
                'total': order['total_amount'],
                'status': order['status']
            },
            'success': True
        }), 200
    
    conn.close()
    # Return empty order if none exists
    return jsonify({
        'result': {
            'user_id': user_id,
            'items': [],
            'total': 0,
            'status': 'pending'
        },
        'success': True
    }), 200

@app.route('/api/order/add-item', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    auth_header = request.headers.get('Authorization', '')
    user_id = get_user_id_from_auth(auth_header)
    
    if not user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.form
    product_id = data.get('product_id')
    qty = int(data.get('qty', 1))
    unit_price = float(data.get('unit_price', 99.99))
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get or create pending order for user
    cursor.execute("""
        SELECT id, total_amount FROM orders
        WHERE user_id = ? AND status = 'pending'
        ORDER BY order_date DESC
        LIMIT 1
    """, (user_id,))
    
    order = cursor.fetchone()
    
    if not order:
        # Create new order
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, status)
            VALUES (?, 0, 'pending')
        """, (user_id,))
        order_id = cursor.lastrowid
        total_amount = 0
    else:
        order_id = order['id']
        total_amount = order['total_amount']
    
    # Add item to order
    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, (order_id, product_id, qty, unit_price))
    
    # Update order total
    new_total = total_amount + (unit_price * qty)
    cursor.execute("""
        UPDATE orders SET total_amount = ? WHERE id = ?
    """, (new_total, order_id))
    
    conn.commit()
    
    # Fetch updated order
    cursor.execute("""
        SELECT id, user_id, total_amount, status FROM orders WHERE id = ?
    """, (order_id,))
    updated_order = cursor.fetchone()
    
    cursor.execute("""
        SELECT id, product_id, quantity, unit_price FROM order_items WHERE order_id = ?
    """, (order_id,))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'result': {
            'id': updated_order['id'],
            'user_id': updated_order['user_id'],
            'items': items,
            'total': updated_order['total_amount'],
            'status': updated_order['status']
        },
        'success': True
    }), 200

@app.route('/api/order/update', methods=['POST'])
def update_order():
    """Update order items"""
    auth_header = request.headers.get('Authorization', '')
    user_id = get_user_id_from_auth(auth_header)
    
    if not user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, total_amount FROM orders
        WHERE user_id = ? AND status = 'pending'
        ORDER BY order_date DESC
        LIMIT 1
    """, (user_id,))
    
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'success': False, 'message': 'No pending order'}), 404
    
    cursor.execute("""
        SELECT id, product_id, quantity, unit_price FROM order_items WHERE order_id = ?
    """, (order['id'],))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'result': {
            'id': order['id'],
            'user_id': user_id,
            'items': items,
            'total': order['total_amount'],
            'status': order['status']
        },
        'success': True
    }), 200

@app.route('/api/order/checkout', methods=['POST'])
def checkout():
    """Checkout order"""
    auth_header = request.headers.get('Authorization', '')
    user_id = get_user_id_from_auth(auth_header)
    
    if not user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get pending order
    cursor.execute("""
        SELECT id, total_amount FROM orders
        WHERE user_id = ? AND status = 'pending'
        ORDER BY order_date DESC
        LIMIT 1
    """, (user_id,))
    
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'success': False, 'message': 'No pending order'}), 404
    
    # Update order status to completed
    cursor.execute("""
        UPDATE orders SET status = 'completed' WHERE id = ?
    """, (order['id'],))
    
    conn.commit()
    
    # Fetch final order
    cursor.execute("""
        SELECT id, user_id, total_amount, status FROM orders WHERE id = ?
    """, (order['id'],))
    final_order = cursor.fetchone()
    
    cursor.execute("""
        SELECT id, product_id, quantity, unit_price FROM order_items WHERE order_id = ?
    """, (order['id'],))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'result': {
            'id': final_order['id'],
            'user_id': final_order['user_id'],
            'items': items,
            'total': final_order['total_amount'],
            'status': final_order['status']
        },
        'success': True,
        'message': 'Order processed'
    }), 200

if __name__ == '__main__':
    print("Order Service starting on 0.0.0.0:5010", flush=True)
    app.run(
        host='0.0.0.0', 
        port=5010, 
        debug=True
    )
