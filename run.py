from app import create_app, db
from app.models import Product

app = create_app()

def add_sample_products():
    sample_products = [
        {
            'name': 'iPhone 16 Pro',
            'description': 'Latest smartphone with advanced features.',
            'price': 799.99,
            'image_url': 'https://d2xamzlzrdbdbn.cloudfront.net/products/d256f9d0-29b8-406d-a77c-fe2cac37492324111046_416x416.jpg'
        },
        {
            'name': 'Macbook Pro',
            'description': 'High-performance laptop for professionals.',
            'price': 1299.99,
            'image_url': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mbp14-m3-max-pro-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830118'
        },
        {
            'name': 'Apple Airpods Pro',
            'description': 'True wireless earbuds with noise cancellation.',
            'price': 149.99,
            'image_url': 'https://media.croma.com/image/upload/v1694672652/Croma%20Assets/Entertainment/Wireless%20Earbuds/Images/301165_xzuxl0.png'
        },
        {
            'name': 'Apple Watch Series 9',
            'description': 'Fitness tracker and smartwatch with heart rate monitor.',
            'price': 199.99,
            'image_url': 'https://rukminim2.flixcart.com/image/850/1000/xif0q/smartwatch/2/r/t/45-mrmu3hn-a-ios-apple-yes-original-imagte7mvmg7h5wt.jpeg?q=90&crop=false'
        },
        {
            'name': 'Cannon EOS R100',
            'description': 'High-resolution digital camera for photography enthusiasts.',
            'price': 649.99,
            'image_url': 'https://www.justcanon.in/cdn/shop/files/R100a.jpg?v=1718108847'
        }
    ]

    for product_data in sample_products:
        product = Product.query.filter_by(name=product_data['name']).first()
        if product is None:
            new_product = Product(**product_data)
            db.session.add(new_product)
    
    db.session.commit()
    print("Sample products added to the database.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_products()
    app.run(debug=True)
