from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database path
DB_PATH = '/data/user.db'

def init_db():
    """Initialize database with schema"""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,     
        password TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(create_user_table_query)
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Default home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'User Service is running'}), 200

@app.route('/api/user/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    print("Login attempt: username=%s, password=%s" % (username, password))
    
    if user and user['password'] == password:
        return jsonify({
            'api_key': 'mock-api-key-12345',
            'user_id': user['id'],
            'success': True
        }), 200
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/user/<username>/exist', methods=['GET'])
def user_exists(username):
    """Check if user exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({'exists': True}), 200
    return jsonify({'exists': False}), 404

@app.route('/api/user/create', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({'success': False, 'message': 'User exists'}), 400
    
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password, first_name, last_name))
        conn.commit()
        
        new_user_id = cursor.lastrowid
        
        return jsonify({
            'result': {
                'id': new_user_id,
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            },
            'success': True
        }), 201
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/user', methods=['GET'])
def get_user():
    """Get current user"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Basic '):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # For now, return hardcoded user (would need proper token parsing in production)
    # The API key is used for authentication, we'd need to store sessions
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email, first_name, last_name FROM users LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'result': dict(user),
            'success': True
        }), 200
    
    return jsonify({'success': False, 'message': 'User not found'}), 404

if __name__ == '__main__':
    print("User Service starting on 0.0.0.0:5010")
    app.run(
        host='0.0.0.0', 
        port=5010, 
        debug=True
    )
