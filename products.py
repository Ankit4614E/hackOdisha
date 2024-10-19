sample_products = [
        {
            'name': 'iPhone 16 Pro',
            'short_description': 'Latest smartphone with advanced features',
        'long_description': '''
        <p>Experience the future of mobile technology with Smartphone X. This cutting-edge device offers:</p>
        <ul>
            <li>6.5-inch OLED display with 120Hz refresh rate</li>
            <li>5G connectivity for lightning-fast internet speeds</li>
            <li>64MP quad-camera system for stunning photos and videos</li>
            <li>5000mAh battery with fast charging capability</li>
            <li>8GB RAM and 256GB storage for smooth multitasking</li>
        </ul>
        <p>Whether you're a photography enthusiast, a mobile gamer, or a busy professional, Smartphone X has everything you need to stay connected and productive.</p>
        ''',
            'price': 799.99,
            'image_url': 'https://d2xamzlzrdbdbn.cloudfront.net/products/d256f9d0-29b8-406d-a77c-fe2cac37492324111046_416x416.jpg'
        },
        {
            'name': 'Macbook Pro',
            'short_description': 'Latest smartphone with advanced features',
        'long_description': '''
        <p>Experience the future of mobile technology with Smartphone X. This cutting-edge device offers:</p>
        <ul>
            <li>6.5-inch OLED display with 120Hz refresh rate</li>
            <li>5G connectivity for lightning-fast internet speeds</li>
            <li>64MP quad-camera system for stunning photos and videos</li>
            <li>5000mAh battery with fast charging capability</li>
            <li>8GB RAM and 256GB storage for smooth multitasking</li>
        </ul>
        <p>Whether you're a photography enthusiast, a mobile gamer, or a busy professional, Smartphone X has everything you need to stay connected and productive.</p>
        ''',
            'price': 1299.99,
            'image_url': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mbp14-m3-max-pro-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830118'
        },
        {
            'name': 'Apple Airpods Pro',
            'short_description': 'Latest smartphone with advanced features',
        'long_description': '''
        <p>Experience the future of mobile technology with Smartphone X. This cutting-edge device offers:</p>
        <ul>
            <li>6.5-inch OLED display with 120Hz refresh rate</li>
            <li>5G connectivity for lightning-fast internet speeds</li>
            <li>64MP quad-camera system for stunning photos and videos</li>
            <li>5000mAh battery with fast charging capability</li>
            <li>8GB RAM and 256GB storage for smooth multitasking</li>
        </ul>
        <p>Whether you're a photography enthusiast, a mobile gamer, or a busy professional, Smartphone X has everything you need to stay connected and productive.</p>
        ''',
            'price': 149.99,
            'image_url': 'https://media.croma.com/image/upload/v1694672652/Croma%20Assets/Entertainment/Wireless%20Earbuds/Images/301165_xzuxl0.png'
        },
        {
            'name': 'Apple Watch Series 9',
            'short_description': 'Latest smartphone with advanced features',
        'long_description': '''
        <p>Experience the future of mobile technology with Smartphone X. This cutting-edge device offers:</p>
        <ul>
            <li>6.5-inch OLED display with 120Hz refresh rate</li>
            <li>5G connectivity for lightning-fast internet speeds</li>
            <li>64MP quad-camera system for stunning photos and videos</li>
            <li>5000mAh battery with fast charging capability</li>
            <li>8GB RAM and 256GB storage for smooth multitasking</li>
        </ul>
        <p>Whether you're a photography enthusiast, a mobile gamer, or a busy professional, Smartphone X has everything you need to stay connected and productive.</p>
        ''',
            'price': 199.99,
            'image_url': 'https://rukminim2.flixcart.com/image/850/1000/xif0q/smartwatch/2/r/t/45-mrmu3hn-a-ios-apple-yes-original-imagte7mvmg7h5wt.jpeg?q=90&crop=false'
        },
        {
            'name': 'Cannon EOS R100',
             'short_description': 'Latest smartphone with advanced features',
        'long_description': '''
        <p>Experience the future of mobile technology with Smartphone X. This cutting-edge device offers:</p>
        <ul>
            <li>6.5-inch OLED display with 120Hz refresh rate</li>
            <li>5G connectivity for lightning-fast internet speeds</li>
            <li>64MP quad-camera system for stunning photos and videos</li>
            <li>5000mAh battery with fast charging capability</li>
            <li>8GB RAM and 256GB storage for smooth multitasking</li>
        </ul>
        <p>Whether you're a photography enthusiast, a mobile gamer, or a busy professional, Smartphone X has everything you need to stay connected and productive.</p>
        ''',
            'price': 649.99,
            'image_url': 'https://www.justcanon.in/cdn/shop/files/R100a.jpg?v=1718108847'
    }
]

import random
def generate_fake_reviews(num_reviews):
    reviews = []
    for _ in range(num_reviews):
        reviews.append({
            'user_name': f"User{random.randint(1, 1000)}",
            'rating': random.randint(1, 5),
            'comment': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        })
    return reviews

# Add fake reviews and calculate average rating for each product
for product in sample_products:
    num_reviews = random.randint(5, 50)
    product['reviews'] = generate_fake_reviews(num_reviews)
    product['rating'] = round(sum(review['rating'] for review in product['reviews']) / num_reviews, 1)
    product['review_count'] = num_reviews
