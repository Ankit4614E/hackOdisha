// /js/order-confirmation.js

document.addEventListener('DOMContentLoaded', () => {
    const currentOrder = JSON.parse(localStorage.getItem('currentOrder'));

    if (!currentOrder) {
        // If no order found, redirect to home or basket
        alert('No order found. Redirecting to Home.');
        window.location.href = 'index.html';
        return;
    }

    displayConfirmationMessage(currentOrder);
    displayOrderDetails(currentOrder);

    // Optionally, clear the current order from localStorage after displaying
    // Uncomment the line below if you want to clear the order after confirmation
    // localStorage.removeItem('currentOrder');
});

// Function to display a confirmation message
function displayConfirmationMessage(order) {
    const confirmationContainer = document.getElementById('confirmation-message');

    const message = document.createElement('div');
    message.className = 'text-center';

    const checkIcon = document.createElement('svg');
    checkIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    checkIcon.setAttribute('class', 'h-12 w-12 text-green-500 mx-auto');
    checkIcon.setAttribute('fill', 'none');
    checkIcon.setAttribute('viewBox', '0 0 24 24');
    checkIcon.setAttribute('stroke', 'currentColor');
    checkIcon.innerHTML = `
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
    `;
    message.appendChild(checkIcon);

    const thankYou = document.createElement('h2');
    thankYou.className = 'text-2xl sm:text-3xl font-bold mt-4';
    thankYou.textContent = 'Thank you for your order!';
    message.appendChild(thankYou);

    const orderNumber = document.createElement('p');
    orderNumber.className = 'mt-2 text-gray-600';
    orderNumber.textContent = `Your order number is ${order.orderNumber}. We have emailed your order confirmation, and will send you an update when your order has shipped.`;
    message.appendChild(orderNumber);

    confirmationContainer.appendChild(message);
}

// Function to display order details and shipping address
function displayOrderDetails(order) {
    const orderDetailsContainer = document.getElementById('order-details');
    const confirmationTotal = document.getElementById('confirmation-total');

    // Shipping Address
    const addressSection = document.createElement('div');
    addressSection.className = 'mb-6';
    addressSection.innerHTML = `
        <h3 class="text-lg font-semibold mb-2">Shipping Address</h3>
        <p>${order.name}</p>
        <p>${order.address}</p>
        <p>${order.city}, ${order.state} - ${order.zip}</p>
        <p>Phone: ${order.phone}</p>
    `;
    orderDetailsContainer.appendChild(addressSection);

    // Order Items
    order.items.forEach(item => {
        const listItem = document.createElement('li');
        listItem.className = 'flex justify-between items-center';

        // Item Name and Quantity
        const itemInfo = document.createElement('div');
        itemInfo.innerHTML = `<span class="font-medium">${item.name}</span> × <span>${item.quantity}</span>`;
        listItem.appendChild(itemInfo);

        // Item Total Price
        const itemTotal = document.createElement('span');
        const totalItemPrice = item.price * item.quantity;
        itemTotal.textContent = `₹${totalItemPrice.toFixed(2)}`;
        listItem.appendChild(itemTotal);

        orderDetailsContainer.appendChild(listItem);
    });

    // Total Price
    confirmationTotal.textContent = `Total: ₹${order.total.toFixed(2)}`;
}
