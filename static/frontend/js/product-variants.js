document.addEventListener('DOMContentLoaded', function() {
    let selectedVariant = {
        size: '',
        color: '',
        price: null,
        stock: null,
        sku: null
    };

    // Function to fetch variant details
    async function getVariantDetails(size, color) {
        const response = await fetch(`/api/products/variant/?product_id=${productId}&size=${size}&color=${color}`);
        return await response.json();
    }

    // Handle variant selection
    document.querySelectorAll('.variant-select').forEach(select => {
        select.addEventListener('change', async function() {
            const type = this.dataset.type;
            selectedVariant[type] = this.value;

            // Get variant details if both size and color are selected
            if (selectedVariant.size && selectedVariant.color) {
                const variant = await getVariantDetails(selectedVariant.size, selectedVariant.color);
                if (variant) {
                    document.getElementById('variant-price').textContent = formatPrice(variant.selling_price);
                    document.getElementById('variant-stock').textContent = variant.stock;
                    document.getElementById('variant-sku').value = variant.sku;
                }
            }

            // Enable/disable add to cart button based on selection
            const addToCartBtn = document.querySelector('.add-to-cart-btn');
            addToCartBtn.disabled = !(selectedVariant.size && selectedVariant.color);
        });
    });
}); 