from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# Mock user database
USERS = {
    'john': {
        'username': 'john',
        'password': 'password123',
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'id': '1'
    }
}

API_KEY = 'mock-api-key-12345'


# defualt home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'User Service is running'}), 200

@app.route('/api/user/login', methods=['POST'])
def login():
    """Mock login endpoint"""
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    user = USERS.get(username)
    print("Login attempt: username=%s, password=%s" % (username, password))
    if user and user['password'] == password:
        return jsonify({
            'api_key': API_KEY,
            'user_id': user['id'],
            'success': True
        })
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/user/<username>/exist', methods=['GET'])
def user_exists(username):
    """Check if user exists"""
    if username in USERS:
        return jsonify({'exists': True}), 200
    return jsonify({'exists': False}), 404

@app.route('/api/user/create', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.form
    username = data.get('username')
    
    if username in USERS:
        return jsonify({'success': False, 'message': 'User exists'}), 400
    
    new_user = {
        'username': username,
        'email': data.get('email'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'password': data.get('password'),
        'id': str(len(USERS) + 1)
    }
    USERS[username] = new_user
    
    return jsonify({
        'result': new_user,
        'success': True
    })

@app.route('/api/user', methods=['GET'])
def get_user():
    """Get current user (mock implementation)"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Basic '):
        return jsonify({
            'result': {
                'id': '1',
                'username': 'john',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            'success': True
        })
    return jsonify({'success': False, 'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    print("User Service starting on 0.0.0.0:5012")
    app.run(
        host='0.0.0.0', 
        port=5012, 
        debug=True
    )
