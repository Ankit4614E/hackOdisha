  let map, marker;

  // Initialize map when location icon is clicked
  document.getElementById("location-icon").addEventListener("click", () => {
      document.getElementById("map-container").classList.remove("hidden");
      initMap(); // Start the map API when the icon is clicked
  });

  function initMap() {
      const defaultLocation = { lat: 20.2961, lng: 85.8245 }; // Bhubaneswar coordinates
      map = new google.maps.Map(document.getElementById("map"), {
          center: defaultLocation,
          zoom: 13,
      });

      marker = new google.maps.Marker({
          position: defaultLocation,
          map: map,
          draggable: true,
      });

      // Add click listener to update the marker's position when the map is clicked
      map.addListener("click", (event) => {
          marker.setPosition(event.latLng);
          updateLocationInfo();
      });

      // Update location info when the marker is dragged and dropped
      marker.addListener("dragend", updateLocationInfo);

      // Add click listener for the confirm location button
      document.getElementById("confirm-location").addEventListener("click", () => {
          updateLocationInfo();
          alert("Location confirmed!");
      });

      // Initialize with the default location info
      updateLocationInfo();
  }

  function updateLocationInfo() {
      const position = marker.getPosition();
      const geocoder = new google.maps.Geocoder();

      geocoder.geocode({ location: position }, (results, status) => {
          if (status === "OK" && results[0]) {
              const address = results[0].formatted_address;
              document.getElementById("selected-location").textContent = address;
          } else {
              document.getElementById("selected-location").textContent = "Unable to determine address";
          }
      });
  }
document.addEventListener('DOMContentLoaded', () => {
    // Initialize basket and wishlist from local storage
    const basket = JSON.parse(localStorage.getItem('basket')) || [];
    const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    updateBasketCount();
    updateWishlistIcons();

    // Handle Add Button Clicks
    const addButtons = document.querySelectorAll('.add-button');

    addButtons.forEach(button => {
        let quantity = 1; // Initialize quantity variable
    
        const quantityControls = button.nextElementSibling;
        const productName = button.getAttribute('data-product');
        const productPrice = parseFloat(button.getAttribute('data-price'));
        const productImage = button.getAttribute('data-image');
    
        button.addEventListener('click', () => {
            if (quantityControls.classList.contains('hidden')) {
                // Show the quantity controls next to the "Add" button
                quantityControls.classList.remove('hidden');
                quantityControls.querySelector('.quantity').textContent = '1'; // Reset quantity to 1
    
                // Handle the - and + button click events
                const decreaseButton = quantityControls.querySelector('.decrease-button');
                const increaseButton = quantityControls.querySelector('.increase-button');
                const quantityElement = quantityControls.querySelector('.quantity');
    
                decreaseButton.addEventListener('click', () => {
                    quantity = parseInt(quantityElement.textContent);
                    if (quantity > 1) {
                        quantityElement.textContent = quantity - 1;
                    }
                });
    
                increaseButton.addEventListener('click', () => {
                    quantity = parseInt(quantityElement.textContent);
                    quantityElement.textContent = quantity + 1;
                });
            } else {
                // Add product to basket
                quantity = parseInt(quantityControls.querySelector('.quantity').textContent);
                addToBasket(productName, productPrice, productImage, quantity);
                quantityControls.classList.add('hidden'); // Hide quantity controls
            }
        });
    });

    // Handle Wishlist Heart Button Clicks
    const heartButtons = document.querySelectorAll('.heart-button');

    heartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productName = button.getAttribute('data-product');
            toggleWishlist(productName, button);
        });
    });

    // Function to toggle wishlist (add/remove)
    function toggleWishlist(productName, button) {
        const heartIcon = button.querySelector('.heart-icon');
        if (wishlist.includes(productName)) {
            wishlist.splice(wishlist.indexOf(productName), 1);
            heartIcon.classList.remove('text-red-500');
            heartIcon.classList.add('text-white');
            alert(`${productName} removed from wishlist.`);
        } else {
            wishlist.push(productName);
            heartIcon.classList.remove('text-white');
            heartIcon.classList.add('text-red-500');
            alert(`${productName} saved for later.`);
        }
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        updateWishlistInBasket(); // Sync with basket page
    }

    // Function to update basket count
    function updateBasketCount() {
        const basketCount = document.getElementById('basket-count');
        const totalItems = basket.reduce((total, item) => total + item.quantity, 0);
        basketCount.textContent = totalItems;
    }

    // Function to update wishlist icons
    function updateWishlistIcons() {
        const heartButtons = document.querySelectorAll('.heart-button');
        heartButtons.forEach(button => {
            const productName = button.getAttribute('data-product');
            const heartIcon = button.querySelector('.heart-icon');
            if (wishlist.includes(productName)) {
                heartIcon.classList.remove('text-white');
                heartIcon.classList.add('text-red-500');
            } else {
                heartIcon.classList.remove('text-red-500');
                heartIcon.classList.add('text-white');
            }
        });
    }

    // Function to add item to basket
    function addToBasket(productName, productPrice, productImage, quantity) {
        const existingItem = basket.find(item => item.name === productName);
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            basket.push({ name: productName, price: productPrice, image: productImage, quantity: quantity });
        }
        localStorage.setItem('basket', JSON.stringify(basket));
        updateBasketCount();
        alert(`${productName} added to basket.`);
    }
    // Function to update the wishlist items in the basket page
    function updateWishlistInBasket() {
        // Sync wishlist with basket page
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }
});
