from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.seller import bp
from app.models import Seller, Product, Order
from app.seller.forms import SellerLoginForm, SellerRegistrationForm, ProductForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and isinstance(current_user, Seller):
        return redirect(url_for('seller.dashboard'))
    form = SellerLoginForm()
    if form.validate_on_submit():
        seller = Seller.query.filter_by(username=form.username.data).first()
        if seller is None or not seller.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('seller.login'))
        login_user(seller, remember=form.remember_me.data)
        return redirect(url_for('seller.dashboard'))
    return render_template('seller/login.html', title='Seller Login', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and isinstance(current_user, Seller):
        return redirect(url_for('seller.dashboard'))
    form = SellerRegistrationForm()
    if form.validate_on_submit():
        seller = Seller(username=form.username.data, email=form.email.data,
                        company_name=form.company_name.data)
        seller.set_password(form.password.data)
        db.session.add(seller)
        db.session.commit()
        flash('Congratulations, you are now a registered seller!')
        return redirect(url_for('seller.login'))
    return render_template('seller/register.html', title='Register as Seller', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Seller):
        flash('Access denied. This area is for sellers only.')
        return redirect(url_for('main.index'))
    return render_template('seller/dashboard.html', seller_name=current_user.username)

@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not isinstance(current_user, Seller):
        flash('Access denied. This area is for sellers only.')
        return redirect(url_for('main.index'))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data,
                          price=form.price.data, image_url=form.image_url.data,
                          seller_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('seller.dashboard'))
    return render_template('seller/add_product.html', title='Add Product', form=form)

@bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not isinstance(current_user, Seller):
        flash('Access denied. This area is for sellers only.')
        return redirect(url_for('main.index'))
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        flash('You can only edit your own products.')
        return redirect(url_for('seller.dashboard'))
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image_url = form.image_url.data
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('seller.dashboard'))
    return render_template('seller/edit_product.html', title='Edit Product', form=form, product=product)

@bp.route('/orders')
@login_required
def orders():
    if not isinstance(current_user, Seller):
        flash('Access denied. This area is for sellers only.')
        return redirect(url_for('main.index'))
    orders = Order.query.filter_by(seller_id=current_user.id).all()
    return render_template('seller/orders.html', title='Seller Orders', orders=orders)

@bp.route('/accept_order/<int:id>', methods=['POST'])
@login_required
def accept_order(id):
    if not isinstance(current_user, Seller):
        flash('Access denied. This area is for sellers only.')
        return redirect(url_for('main.index'))
    order = Order.query.get_or_404(id)
    if order.seller_id != current_user.id:
        flash('You can only manage your own orders.')
        return redirect(url_for('seller.orders'))
    
    order.status = 'accepted'
    db.session.commit()
    flash('Order accepted successfully!')
    return redirect(url_for('seller.orders'))

@bp.route('/reject_order/<int:id>', methods=['POST'])
@login_required
def reject_order(id):
    if not isinstance(current_user, Seller):
        flash('Access denied. This area is for sellers only.')
        return redirect(url_for('main.index'))
    order = Order.query.get_or_404(id)
    if order.seller_id != current_user.id:
        flash('You can only manage your own orders.')
        return redirect(url_for('seller.orders'))
    
    order.status = 'rejected'
    db.session.commit()
    flash('Order rejected successfully!')
    return redirect(url_for('seller.orders'))
