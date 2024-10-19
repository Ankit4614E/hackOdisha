document.addEventListener('DOMContentLoaded', () => {
    const basket = JSON.parse(localStorage.getItem('basket')) || [];
    const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];

    displayBasketItems();
    displayWishlistItems();
    updateBasketCount();

// Function to display items in the basket
function displayBasketItems() {
    const basketItemsContainer = document.getElementById('basket-items');
    basketItemsContainer.innerHTML = '';

    if (basket.length === 0) {
        basketItemsContainer.innerHTML = '<li class="text-gray-500">No items in the basket.</li>';
    } else {
        let totalPrice = 0;
        basket.forEach((item, index) => {
            const listItem = document.createElement('li');
            listItem.className = 'bg-white p-2 rounded shadow mb-2 flex items-center'; // Added flex here

            // Product image
            const productImage = document.createElement('img');
            productImage.src = item.image;
            productImage.alt = item.name;
            productImage.className = 'w-20 h-20 object-cover mr-4';
            listItem.appendChild(productImage);

            // Product name, quantity, and buttons container
            const productInfo = document.createElement('div');
            productInfo.className = 'flex-1 flex justify-between items-start'; // Ensure content is spaced between image and buttons

            const nameAndQuantityContainer = document.createElement('div');
            nameAndQuantityContainer.className = 'flex-1';

            // Product name
            const itemName = document.createElement('span');
            itemName.textContent = item.name;
            nameAndQuantityContainer.appendChild(itemName);

            // Quantity input and update button
            const quantityContainer = document.createElement('div');
            quantityContainer.className = 'flex items-center mt-2';

            const quantityInput = document.createElement('input');
            quantityInput.type = 'number';
            quantityInput.min = 1;
            quantityInput.value = item.quantity;
            quantityInput.className = 'w-12 pl-2 py-1 border border-gray-300 rounded';
            quantityContainer.appendChild(quantityInput);

            nameAndQuantityContainer.appendChild(quantityContainer);
            productInfo.appendChild(nameAndQuantityContainer);

            // Price and buttons container (update, remove)
            const buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'flex flex-col items-end'; // Stack buttons vertically

            // Update button
            const updateButton = document.createElement('button');
            updateButton.textContent = 'Update';
            updateButton.className = 'bg-green-500 text-white px-2 py-1 rounded mb-2 w-full';
            updateButton.addEventListener('click', () => {
                const newQuantity = parseInt(quantityInput.value);
                if (newQuantity > 0) {
                    item.quantity = newQuantity;
                    localStorage.setItem('basket', JSON.stringify(basket));
                    displayBasketItems();
                    updateBasketCount();
                }
            });
            buttonsContainer.appendChild(updateButton);

            // Remove button
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.className = 'bg-red-500 text-white px-2 py-1 rounded w-full';
            removeButton.addEventListener('click', () => {
                removeFromBasket(item.name);
            });
            buttonsContainer.appendChild(removeButton);

            productInfo.appendChild(buttonsContainer);
            listItem.appendChild(productInfo);

            // Product price below the quantity
            const itemPrice = document.createElement('span');
            const totalItemPrice = item.price * item.quantity;
            totalPrice += totalItemPrice;
            itemPrice.textContent = `Price: ₹${totalItemPrice.toFixed(2)}`;
            listItem.appendChild(itemPrice);

            basketItemsContainer.appendChild(listItem);
        });

        const totalPriceElement = document.createElement('li');
        totalPriceElement.className = 'font-bold text-right mt-4';
        totalPriceElement.textContent = `Total Price: ₹${totalPrice.toFixed(2)}`;
        basketItemsContainer.appendChild(totalPriceElement);

        // Add checkout button
        const checkoutButton = document.createElement('button');
        checkoutButton.textContent = 'Proceed to Checkout';
        checkoutButton.className = 'bg-blue-500 text-white py-2 px-4 rounded mt-4 w-full hover:bg-blue-600';
        checkoutButton.addEventListener('click', () => {
            window.location.href = 'checkout.html'; // Redirect to checkout page
        });
        basketItemsContainer.appendChild(checkoutButton);
    }
}

    // Function to display wishlist items in the "Save for Later" section
    function displayWishlistItems() {
        const wishlistItemsContainer = document.getElementById('wishlist-items');
        wishlistItemsContainer.innerHTML = '';

        if (wishlist.length === 0) {
            wishlistItemsContainer.innerHTML = '<li class="text-gray-500">No items saved for later.</li>';
        } else {
            wishlist.forEach(productName => {
                const listItem = document.createElement('li');
                listItem.className = 'bg-gray-100 p-2 rounded shadow mb-2 flex justify-between items-center';
                listItem.textContent = productName;

                const removeButton = document.createElement('button');
                removeButton.textContent = 'Remove';
                removeButton.className = 'bg-red-500 text-white px-2 rounded ml-2';
                removeButton.addEventListener('click', () => {
                    removeFromWishlist(productName);
                });
                listItem.appendChild(removeButton);
                wishlistItemsContainer.appendChild(listItem);
            });
        }
    }

    // Function to remove item from basket
    function removeFromBasket(productName) {
        const index = basket.findIndex(item => item.name === productName);
        if (index > -1) {
            basket.splice(index, 1);
            localStorage.setItem('basket', JSON.stringify(basket));
            displayBasketItems();
            updateBasketCount();
        }
    }

    // Function to remove item from wishlist and update heart icon on index page
    function removeFromWishlist(productName) {
        const index = wishlist.indexOf(productName);
        if (index > -1) {
            wishlist.splice(index, 1);
            localStorage.setItem('wishlist', JSON.stringify(wishlist));
            displayWishlistItems();
            updateHeartIconOnIndexPage(productName, false); // Reset heart icon on index page
        }
    }

    // Function to update the heart icon color on the index page
    function updateHeartIconOnIndexPage(productName, isWishlist) {
        const heartButton = document.querySelector(`.heart-button[data-product="${productName}"]`);
        const heartIcon = heartButton.querySelector('.heart-icon');
        if (isWishlist) {
            heartIcon.classList.remove('text-white');
            heartIcon.classList.add('text-red-500');
        } else {
            heartIcon.classList.remove('text-red-500');
            heartIcon.classList.add('text-white');
        }
    }

    // Function to update basket count
    function updateBasketCount() {
        const basketCount = document.getElementById('basket-count');
        const totalItems = basket.reduce((total, item) => total + item.quantity, 0);
        basketCount.textContent = totalItems;
    }
});
