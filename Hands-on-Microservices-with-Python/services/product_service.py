from flask import Flask, jsonify

app = Flask(__name__)

# Mock products database
PRODUCTS = {
    'laptop-dell': {
        'id': '1',
        'name': 'Dell Laptop',
        'slug': 'laptop-dell',
        'price': '899.99',
        'description': 'High-performance laptop',
        'image': 'laptop.jpg'
    },
    'mouse-wireless': {
        'id': '2',
        'name': 'Wireless Mouse',
        'slug': 'mouse-wireless',
        'price': '29.99',
        'description': 'Ergonomic wireless mouse',
        'image': 'mouse.jpg'
    },
    'keyboard-mechanical': {
        'id': '3',
        'name': 'Mechanical Keyboard',
        'slug': 'keyboard-mechanical',
        'price': '129.99',
        'description': 'RGB mechanical keyboard',
        'image': 'keyboard.jpg'
    }
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({'message': 'Product Service is running'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify({
        'results': list(PRODUCTS.values()),
        'success': True
    })

@app.route('/api/product/<slug>', methods=['GET'])
def get_product(slug):
    """Get single product by slug"""
    product = PRODUCTS.get(slug)
    if product:
        return jsonify({
            'result': product,
            'success': True
        })
    return jsonify({'success': False, 'message': 'Product not found'}), 404

if __name__ == '__main__':
    print("Product Service starting on 0.0.0.0:5010")
    app.run(
        host='0.0.0.0', 
        port=5010, 
        debug=True
    )
