from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.main import bp
from app.models import Product, Order, User
from datetime import datetime
from app.main.forms import RegistrationForm, LoginForm

@bp.route('/')
@bp.route('/index')
def index():
    products = Product.query.all()
    return render_template('home.html', title='Home', products=products)

@bp.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    recommended_products = Product.query.filter(Product.id != id).limit(4).all()
    return render_template('product.html', title=product.name, product=product, recommended_products=recommended_products)

@bp.route('/add_to_cart/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    product = Product.query.get_or_404(id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        return jsonify({'success': False, 'message': 'Not enough stock available.'})
    
    order = Order(user_id=current_user.id, product_id=product.id, seller_id=product.seller_id, quantity=quantity)
    db.session.add(order)
    product.stock -= quantity
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Product added to cart successfully.'})

@bp.route('/cart')
@login_required
def cart():
    orders = Order.query.filter_by(user_id=current_user.id, status='pending').all()
    return render_template('cart.html', title='Shopping Cart', orders=orders)

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
