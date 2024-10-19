function addToCart(productId) {
    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product added to cart!');
            updateCartCount();
        }
    });
}

function removeFromCart(productId) {
    fetch('/api/remove-from-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product removed from cart!');
            updateCartCount();
            location.reload();
        }
    });
}

function updateCartCount() {
    fetch('/api/cart-count')
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-count').textContent = data.count;
    });
}

function placeOrder() {
    const modal = document.getElementById('order-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');

    // Simulate order placement and store allocation
    setTimeout(() => {
        modal.classList.remove('flex');
        modal.classList.add('hidden');
        alert('Order placed successfully! A nearby store has accepted your order.');
    }, 5000);
}

const searchInput = document.getElementById('search');
const searchResults = document.getElementById('search-results');

searchInput.addEventListener('input', debounce(function() {
    const query = this.value.trim();
    if (query.length > 2) {
        fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                searchResults.innerHTML = '';
                data.forEach(product => {
                    const div = document.createElement('div');
                    div.className = 'p-2 hover:bg-gray-100 cursor-pointer';
                    div.textContent = `${product.name} - $${product.price.toFixed(2)}`;
                    div.onclick = () => window.location.href = `/product/${product.id}`;
                    searchResults.appendChild(div);
                });
                searchResults.classList.remove('hidden');
            });
    } else {
        searchResults.classList.add('hidden');
    }
}, 300));

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

document.addEventListener('click', function(event) {
    if (!searchResults.contains(event.target) && event.target !== searchInput) {
        searchResults.classList.add('hidden');
    }
});

// Simulate getting user's location
setTimeout(() => {
    document.getElementById('user-location').textContent = 'Delivering to: New York, NY';
}, 2000);

// Initialize cart count on page load
updateCartCount();
