from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user, login_required, login_user, logout_user
from app import db, socketio, csrf
from app.main import bp
from app.models import Product, Order, User, Seller
from datetime import datetime, timedelta
from app.main.forms import RegistrationForm, LoginForm
import traceback
from flask_socketio import emit, join_room
from flask import session

@bp.route('/')
@bp.route('/index')
def index():
    products = Product.query.all()
    return render_template('home.html', title='Home', products=products)

@bp.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    recommended_products = Product.query.filter(Product.id != id).order_by(db.func.random()).limit(4).all()
    return render_template('product.html', title=product.name, product=product, recommended_products=recommended_products)

@bp.route('/add_to_cart/<int:id>', methods=['POST'])
@login_required
@csrf.exempt  # Exempt this route from CSRF protection
def add_to_cart(id):
    product = Product.query.get_or_404(id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        return jsonify({'success': False, 'message': 'Not enough stock available.'})
    
    cart_item = Order.query.filter_by(user_id=current_user.id, product_id=product.id, status='cart').first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Order(user_id=current_user.id, product_id=product.id, quantity=quantity, status='cart')
        db.session.add(cart_item)
    
    product.stock -= quantity
    db.session.commit()
    
    cart_count = Order.query.filter_by(user_id=current_user.id, status='cart').count()
    return jsonify({'success': True, 'message': 'Product added to cart successfully.', 'cart_count': cart_count})

@bp.route('/cart')
@login_required
def cart():
    cart_items = Order.query.filter_by(user_id=current_user.id, status='cart').all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', title='Shopping Cart', cart_items=cart_items, total=total)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Add this new route to get the current cart count
@bp.route('/cart_count')
@login_required
def cart_count():
    count = Order.query.filter_by(user_id=current_user.id, status='cart').count()
    return jsonify({'count': count})

@socketio.on('join', namespace='/buyer')
def on_join(data):
    room = data['user_id']
    join_room(room)

@bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    try:
        current_app.logger.info(f"Attempting to place order for user {current_user.id}")
        cart_items = Order.query.filter_by(user_id=current_user.id, status='cart').all()
        
        if not cart_items:
            current_app.logger.warning(f"Cart is empty for user {current_user.id}")
            return jsonify({'success': False, 'message': 'Your cart is empty.'})

        total = sum(item.product.price * item.quantity for item in cart_items)
        
        for cart_item in cart_items:
            cart_item.status = 'pending'
            cart_item.created_at = datetime.utcnow()
        
        db.session.commit()
        current_app.logger.info(f"Placed order for user {current_user.id}")

        # Notify all online sellers about the new order
        for item in cart_items:
            socketio.emit('new_order', {
                'order_id': item.id,
                'user_id': current_user.id,
                'user_name': current_user.username,
                'product_name': item.product.name,
                'product_price': item.product.price,
                'quantity': item.quantity,
                'total': item.product.price * item.quantity
            }, namespace='/seller')
        current_app.logger.info(f"Emitted new_order event for user {current_user.id}")

        return jsonify({'success': True, 'message': 'Order placed successfully. We are finding a seller to fulfill your order.'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in place_order: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': 'An error occurred while placing your order. Please try again.'}), 500

@socketio.on('seller_response', namespace='/seller')
def handle_seller_response(data):
    order_id = data['order_id']
    response = data['response']
    seller_id = data['seller_id']

    order = Order.query.get(order_id)
    if order and order.status == 'pending':
        if response == 'accept':
            order.status = 'accepted'
            order.seller_id = seller_id
            db.session.commit()
            seller = Seller.query.get(seller_id)
            socketio.emit('order_accepted', {
                'order_id': order_id,
                'seller_name': seller.company_name,
                'estimated_delivery': (datetime.utcnow() + timedelta(minutes=7)).isoformat()
            }, room=str(order.user_id), namespace='/buyer')
            return {'success': True, 'order': {
                'id': order.id,
                'user_name': order.buyer.username,
                'product_name': order.product.name,
                'product_price': order.product.price,
                'quantity': order.quantity,
                'total': order.product.price * order.quantity
            }}
        elif response == 'decline':
            # If declined, notify other sellers again, excluding the one who just declined
            socketio.emit('new_order', {
                'order_id': order.id,
                'user_id': order.user_id,
                'user_name': order.buyer.username,
                'product_name': order.product.name,
                'product_price': order.product.price,
                'quantity': order.quantity,
                'total': order.product.price * order.quantity
            }, namespace='/seller', skip_sid=request.sid)  # Skip the current seller
            return {'success': True}
    
    return {'success': False, 'message': 'Order not found or already processed'}

@socketio.on('join', namespace='/seller')
def on_seller_join(data):
    seller_id = data['seller_id']
    join_room(seller_id)
