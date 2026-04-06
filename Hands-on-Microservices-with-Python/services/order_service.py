from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Mock orders database (per user)
ORDERS = {
    '1': {
        'user_id': '1',
        'items': [],
        'total': 0
    }
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Order Service is running'}), 200



@app.route('/api/order', methods=['GET'])
def get_order():
    """Get current order"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Basic '):
        return jsonify({
            'result': {
                'user_id': '1',
                'items': [],
                'total': 0
            },
            'success': True
        })
    return jsonify({'success': False, 'message': 'Unauthorized'}), 401

@app.route('/api/order/add-item', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Basic '):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.form
    product_id = data.get('product_id')
    qty = int(data.get('qty', 1))
    
    order = ORDERS.get('1', {'user_id': '1', 'items': [], 'total': 0})
    
    # Add item to order
    item = {
        'product_id': product_id,
        'quantity': qty,
        'price': '99.99'
    }
    order['items'].append(item)
    order['total'] = float(order['total']) + (99.99 * qty)
    
    return jsonify({
        'result': order,
        'success': True
    })

@app.route('/api/order/update', methods=['POST'])
def update_order():
    """Update order items"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Basic '):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    order = ORDERS.get('1', {'user_id': '1', 'items': [], 'total': 0})
    return jsonify({
        'result': order,
        'success': True
    })

@app.route('/api/order/checkout', methods=['POST'])
def checkout():
    """Checkout order"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Basic '):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    order = ORDERS.get('1', {'user_id': '1', 'items': [], 'total': 0})
    
    # Clear the order after checkout
    order['items'] = []
    order['total'] = 0
    
    return jsonify({
        'result': order,
        'success': True,
        'message': 'Order processed'
    })

if __name__ == '__main__':
    print("Order Service starting on 0.0.0.0:5010")
    app.run(
        host='0.0.0.0', 
        port=5010, 
        debug=True
    )
