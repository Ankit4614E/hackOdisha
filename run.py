from app import create_app, db, socketio
from app.models import Product, Seller, User, Review
from products import sample_products
import random

app = create_app()

def add_sample_data():
    # Check if there's already data in the database
    if User.query.first() is not None:
        print("Sample data already exists. Skipping...")
        return

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
        buyer = User(username='buyer1', email='buyer1@example.com')
        buyer.set_password('password')
        db.session.add(buyer)

    db.session.commit()

    # Verify that the buyer was created successfully
    buyer = User.query.filter_by(username='buyer1').first()
    if buyer is None:
        print("Failed to create sample buyer")
        return

    # Add sample products
    for product_data in sample_products:
        product = Product.query.filter_by(name=product_data['name']).first()
        if product is None:
            new_product = Product(
                name=product_data['name'],
                short_description=product_data['short_description'],
                long_description=product_data['long_description'],
                price=round(product_data['price'] * 75, 2),  # Convert USD to INR
                image_url=product_data['image_url'],
                stock=random.randint(10, 100),
                rating=product_data['rating'],
                review_count=product_data['review_count']
            )
            new_product.seller = Seller.query.first()  # Assign to the first seller for simplicity
            db.session.add(new_product)
            db.session.flush()  # Flush to get the product ID

            # Add reviews
            for review_data in product_data['reviews']:
                review = Review(
                    user_id=buyer.id,
                    product_id=new_product.id,
                    rating=review_data['rating'],
                    comment=review_data['comment']
                )
                db.session.add(review)

    try:
        db.session.commit()
        print("Sample data added to the database.")
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_data()
    socketio.run(app, debug=True)
