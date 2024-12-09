function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
    });
}

function formatPrice(price) {
    return '৳' + parseFloat(price).toFixed(2);
}

function updateCartDisplay(cartData) {
    const cartItemsContainer = document.querySelector('.side-cart-items');
    const cartTotalElement = document.querySelector('.main-total-cart span');
    const cartCountElement = document.querySelector('.main-cart-title span');
    
    // Update cart count in header
    cartCountElement.textContent = `(${cartData.total_items} Items)`;
    
    // Clear existing items
    cartItemsContainer.innerHTML = '';
    
    // Add each item to the cart display
    cartData.items.forEach(item => {
        const product = item.product;
        const itemHtml = `
            <div class="cart-item">
                <div class="cart-product-img">
                    ${product.primary_image ? 
                        `<img src="${product.primary_image.image}" alt="${product.name}">` :
                        '<img src="https://via.placeholder.com/150x150?text=No+Image" alt="Default Image">'
                    }
                </div>
                <div class="cart-text">
                    <h4>${product.name}</h4>
                    <div class="qty-group">
                        <div class="quantity buttons_added">
                            <input type="button" value="-" class="minus minus-btn" data-item="${item.id}">
                            <input type="number" step="1" name="quantity" value="${item.quantity}" 
                                   class="input-text qty text" data-item="${item.id}">
                            <input type="button" value="+" class="plus plus-btn" data-item="${item.id}">
                        </div>
                        <div class="cart-item-price">
                            ${formatPrice(product.selling_price)}
                            ${product.discount_percentage > 0 ? 
                                `<span>${formatPrice(product.original_price)}</span>` : 
                                ''
                            }
                        </div>
                    </div>
                    <button type="button" class="cart-close-btn" data-item="${item.id}">
                        <i class="uil uil-multiply"></i>
                    </button>
                </div>
            </div>
        `;
        cartItemsContainer.insertAdjacentHTML('beforeend', itemHtml);
    });
    
    // Update total price
    cartTotalElement.textContent = formatPrice(cartData.total_price);
    
    // Setup quantity controls after updating display
    setupQuantityControls();
}

function fetchCartItems() {
    fetch('/cart/api/list/')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                updateCartDisplay(data[0]);
            }
        })
        .catch(error => console.error('Error fetching cart:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    // Fetch cart items when page loads
    fetchCartItems();

    const addToCartBtn = document.querySelector('.add-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            const productId = this.dataset.product;
            const quantityInput = document.querySelector('.qty.text');
            const quantity = parseInt(quantityInput.value);

            fetch('/cart/api/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: data.error
                    });
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success!',
                        text: 'Item added to cart',
                        timer: 1500
                    });
                    updateCartCount(data.cart_total);
                    fetchCartItems(); // Refresh cart display
                }
            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong! Please try again.'
                });
            });
        });
    }
});

function handleQuantityUpdate(itemId, newQuantity) {
    fetch('/cart/api/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: newQuantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: data.error
            });
            // Reset the quantity input to its previous value
            fetchCartItems();
        } else {
            if (data.message === 'Item removed from cart') {
                fetchCartItems(); // Refresh entire cart
            } else {
                // Update the specific item's subtotal
                const itemPrice = document.querySelector(`[data-item="${itemId}"]`)
                    .closest('.cart-text')
                    .querySelector('.cart-item-price');
                itemPrice.innerHTML = formatPrice(data.item_subtotal);
                
                // Update cart total
                const cartTotalElement = document.querySelector('.main-total-cart span');
                cartTotalElement.textContent = formatPrice(data.cart_total_price);
                
                // Update cart count in header
                updateCartCount(data.cart_total);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Something went wrong! Please try again.'
        });
    });
}

function setupQuantityControls() {
    const cartItemsContainer = document.querySelector('.side-cart-items');
    
    cartItemsContainer.addEventListener('click', function(e) {
        const target = e.target;
        
        // Handle minus button
        if (target.classList.contains('minus-btn')) {
            const itemId = target.dataset.item;
            const quantityInput = target.nextElementSibling;
            const currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
                handleQuantityUpdate(itemId, currentValue - 1);
            } else if (currentValue === 1) {
                // Show confirmation before removing item
                Swal.fire({
                    title: 'Remove Item?',
                    text: "Do you want to remove this item from cart?",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes, remove it!'
                }).then((result) => {
                    if (result.isConfirmed) {
                        handleQuantityUpdate(itemId, 0); // 0 quantity will remove the item
                    }
                });
            }
        }
        
        // Handle plus button
        if (target.classList.contains('plus-btn')) {
            const itemId = target.dataset.item;
            const quantityInput = target.previousElementSibling;
            const currentValue = parseInt(quantityInput.value);
            quantityInput.value = currentValue + 1;
            handleQuantityUpdate(itemId, currentValue + 1);
        }
    });

    // Handle direct input changes
    cartItemsContainer.addEventListener('change', function(e) {
        const target = e.target;
        if (target.classList.contains('qty') && target.classList.contains('text')) {
            const itemId = target.dataset.item;
            const newValue = parseInt(target.value);
            if (newValue < 1) {
                target.value = 1;
                handleQuantityUpdate(itemId, 1);
            } else {
                handleQuantityUpdate(itemId, newValue);
            }
        }
    });
}
