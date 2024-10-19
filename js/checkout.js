// /js/checkout.js

document.addEventListener('DOMContentLoaded', () => {
  const basket = JSON.parse(localStorage.getItem('basket')) || [];

  displayOrderSummary();

  const checkoutForm = document.getElementById('checkout-form');
  checkoutForm.addEventListener('submit', handleCheckout);

  // Function to display order summary
  function displayOrderSummary() {
      const orderSummaryContainer = document.getElementById('order-summary');
      const summaryTotal = document.getElementById('summary-total');
      orderSummaryContainer.innerHTML = '';

      if (basket.length === 0) {
          orderSummaryContainer.innerHTML = '<li class="text-gray-500">Your basket is empty.</li>';
          summaryTotal.textContent = 'Total: ₹0.00';
      } else {
          let totalPrice = 0;
          basket.forEach(item => {
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

              totalPrice += totalItemPrice;
              orderSummaryContainer.appendChild(listItem);
          });

          summaryTotal.textContent = `Total: ₹${totalPrice.toFixed(2)}`;
      }
  }

  // Function to handle checkout form submission
  function handleCheckout(event) {
      event.preventDefault();

      if (basket.length === 0) {
          alert('Your basket is empty. Please add items before proceeding to checkout.');
          return;
      }

      // Collect form data
      const formData = new FormData(checkoutForm);
      const orderDetails = {
          name: formData.get('name'),
          address: formData.get('address'),
          city: formData.get('city'),
          state: formData.get('state'),
          zip: formData.get('zip'),
          phone: formData.get('phone'),
          items: basket,
          total: basket.reduce((total, item) => total + item.price * item.quantity, 0),
          orderDate: new Date().toLocaleString(),
          orderNumber: generateOrderNumber()
      };

      // Save order to localStorage
      localStorage.setItem('currentOrder', JSON.stringify(orderDetails));

      // Clear the basket
      localStorage.removeItem('basket');

      // Redirect to order confirmation page
      window.location.href = 'order-confirmation.html';
  }

  // Function to generate a random order number
  function generateOrderNumber() {
      return 'ORD-' + Math.floor(Math.random() * 1000000);
  }
});
