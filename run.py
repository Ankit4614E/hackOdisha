from app import create_app, db
from app.models import Product, Seller, User
from products import sample_products
from datetime import datetime, timedelta

app = create_app()

def add_sample_data():
    # Add sample sellers
    sellers = [
        {'username': 'seller1', 'email': 'seller1@example.com', 'password': 'password', 'company_name': 'Company A'},
        {'username': 'seller2', 'email': 'seller2@example.com', 'password': 'password', 'company_name': 'Company B'},
        {'username': 'seller3', 'email': 'seller3@example.com', 'password': 'password', 'company_name': 'Company C'},
    ]

    for seller_data in sellers:
        seller = Seller.query.filter_by(username=seller_data['username']).first()
        if seller is None:
            new_seller = Seller(username=seller_data['username'], email=seller_data['email'], company_name=seller_data['company_name'])
            new_seller.set_password(seller_data['password'])
            db.session.add(new_seller)

    # Add a sample buyer
    buyer = User.query.filter_by(username='buyer1').first()
    if buyer is None:
        new_buyer = User(username='buyer1', email='buyer1@example.com')
        new_buyer.set_password('password')
        db.session.add(new_buyer)

    db.session.commit()

    # Add sample products (shared among all sellers)
    for product_data in sample_products:
        product = Product.query.filter_by(name=product_data['name']).first()
        if product is None:
            new_product = Product(**product_data)
            new_product.bid_end_time = datetime.utcnow() + timedelta(days=7)
            db.session.add(new_product)
    
    db.session.commit()
    print("Sample data added to the database.")

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create new tables
        add_sample_data()
    app.run(debug=True)
