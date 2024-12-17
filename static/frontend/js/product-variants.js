document.addEventListener('DOMContentLoaded', function() {
    let selectedVariant = {
        size: '',
        color: '',
        price: null,
        stock: null,
        id: null
    };

    // Function to fetch variant details
    async function getVariantDetails(size, color) {
        try {
            const productId = document.querySelector('.add-variant-cart-btn').dataset.product;
            const response = await fetch(`/products/api/variant/?product_id=${productId}&size=${size}&color=${color}`);
            if (!response.ok) {
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching variant:', error);
            return null;
        }
    }

    // Function to update variant display
    function updateVariantDisplay() {
        const variantDetails = document.getElementById('variant-details');
        const variantInstructions = document.getElementById('variant-instructions');
        const priceElement = document.getElementById('variant-price');
        const stockElement = document.getElementById('variant-stock');
        const addToCartBtn = document.querySelector('.add-variant-cart-btn');
        const orderBtn = document.querySelector('.order-btn');

        if (selectedVariant.size && selectedVariant.color) {
            if (selectedVariant.price !== null) {
                // Show variant details
                variantDetails.style.display = 'block';
                variantInstructions.style.display = 'none';

                priceElement.textContent = selectedVariant.price.toFixed(2);
                
                const isInStock = selectedVariant.stock > 0;
                addToCartBtn.disabled = !isInStock;
                orderBtn.disabled = !isInStock;
                
                if (isInStock) {
                    stockElement.className = 'stock-badge in-stock';
                    stockElement.textContent = `${selectedVariant.stock} in stock`;
                } else {
                    stockElement.className = 'stock-badge out-of-stock';
                    stockElement.textContent = 'Out of Stock';
                }
            } else {
                // Variant not available
                variantDetails.style.display = 'none';
                variantInstructions.style.display = 'block';
                variantInstructions.className = 'variant-message error';
                variantInstructions.innerHTML = '<i class="fas fa-exclamation-circle"></i> This combination is not available';
                addToCartBtn.disabled = true;
                orderBtn.disabled = true;
            }
        } else {
            // Not all options selected
            if (variantDetails) {
                variantDetails.style.display = 'none';
            }
            if (variantInstructions) {
                variantInstructions.style.display = 'block';
                variantInstructions.className = 'variant-message';
                variantInstructions.innerHTML = '<i class="fas fa-info-circle"></i> Please select size and color options';
            }
            if (addToCartBtn) {
                addToCartBtn.disabled = true;
            }
            if (orderBtn) {
                orderBtn.disabled = true;
            }
        }
    }

    // Handle variant selection
    document.querySelectorAll('.variant-select').forEach(input => {
        input.addEventListener('change', async function() {
            const type = this.dataset.type;
            selectedVariant[type] = this.value;

            // Get variant details if both size and color are selected
            if (selectedVariant.size && selectedVariant.color) {
                const variant = await getVariantDetails(selectedVariant.size, selectedVariant.color);
                if (variant) {
                    selectedVariant.price = variant.selling_price;
                    selectedVariant.stock = variant.stock;
                    selectedVariant.id = variant.id;
                } else {
                    selectedVariant.price = null;
                    selectedVariant.stock = 0;
                    selectedVariant.id = null;
                }
            }

            updateVariantDisplay();
        });
    });

    // Handle add to cart for variant products
    const addVariantCartBtn = document.querySelector('.add-variant-cart-btn');
    if (addVariantCartBtn) {
        addVariantCartBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            if (selectedVariant.id) {
                const quantity = document.querySelector('.qty.text').value;
                const data = {
                    product_id: this.dataset.product,
                    variant_id: selectedVariant.id,
                    quantity: quantity
                };
                
                addToCart(data);
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Please select options',
                    text: 'Please select size and color options'
                });
            }
        });
    }

    // Initialize buttons as disabled
    updateVariantDisplay();
});