from flask import Blueprint, render_template, jsonify, request, session
from app.models import Product, User
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@main.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart_items)).all()
    return render_template('cart.html', products=products)

@main.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    cart = session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        session['cart'] = cart
    return jsonify({'success': True})

@main.route('/api/remove-from-cart', methods=['POST'])
def remove_from_cart():
    product_id = request.json.get('product_id')
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
    return jsonify({'success': True})

@main.route('/api/cart-count')
def cart_count():
    cart = session.get('cart', [])
    return jsonify({'count': len(cart)})

@main.route('/api/search')
def search():
    query = request.args.get('q', '')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])
