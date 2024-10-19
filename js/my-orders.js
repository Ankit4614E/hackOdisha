document.addEventListener('DOMContentLoaded', () => {
    const ordersContainer = document.getElementById('orders-container');
    const orders = JSON.parse(localStorage.getItem('orders')) || [];

    if (orders.length === 0) {
        ordersContainer.innerHTML = '<p class="text-gray-500">You have no orders placed yet.</p>';
    } else {
        orders.reverse(); // Show latest orders first
        orders.forEach(order => {
            const orderCard = document.createElement('div');
            orderCard.className = 'bg-white p-4 rounded-lg shadow-md';

            // Order Header
            const orderHeader = document.createElement('div');
            orderHeader.className = 'flex justify-between items-center mb-4';

            const orderInfo = document.createElement('div');
            orderInfo.innerHTML = `
                <span class="font-semibold">Order #${order.orderNumber}</span>
                <span class="text-sm text-gray-600"> - Placed on ${order.orderDate}</span>
            `;
            orderHeader.appendChild(orderInfo);

            const orderStatus = document.createElement('span');
            orderStatus.className = `text-sm font-semibold ${
                order.status === 'Delivered' ? 'text-green-600' :
                order.status === 'Processing' ? 'text-yellow-600' :
                'text-gray-600'
            }`;
            orderStatus.textContent = order.status;
            orderHeader.appendChild(orderStatus);

            orderCard.appendChild(orderHeader);

            // Shipping Address
            const shippingAddress = document.createElement('div');
            shippingAddress.className = 'mb-4';
            shippingAddress.innerHTML = `
                <h3 class="font-medium">Shipping Address</h3>
                <p>${order.name}</p>
                <p>${order.address}</p>
                <p>${order.city}, ${order.state} - ${order.zip}</p>
                <p>Phone: ${order.phone}</p>
            `;
            orderCard.appendChild(shippingAddress);

            // Order Items
            const orderItems = document.createElement('div');
            orderItems.className = 'mb-4';
            orderItems.innerHTML = `<h3 class="font-medium mb-2">Items</h3>`;
            const itemsList = document.createElement('ul');
            itemsList.className = 'space-y-2';
            order.items.forEach(item => {
                const itemLi = document.createElement('li');
                itemLi.className = 'flex justify-between';
                itemLi.innerHTML = `
                    <span>${item.name} × ${item.quantity}</span>
                    <span>₹${(item.price * item.quantity).toFixed(2)}</span>
                `;
                itemsList.appendChild(itemLi);
            });
            orderItems.appendChild(itemsList);
            orderCard.appendChild(orderItems);

            // Order Total
            const orderTotal = document.createElement('div');
            orderTotal.className = 'flex justify-end font-semibold';
            orderTotal.textContent = `Total: ₹${order.total.toFixed(2)}`;
            orderCard.appendChild(orderTotal);

            ordersContainer.appendChild(orderCard);
        });
    }
});
