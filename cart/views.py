from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.urls import reverse
import logging
from products.models import Product
from orders.models import Order, OrderItem
from users.models import Address
from .models import Cart, CartItem
from .serializers import CartSerializer

logger = logging.getLogger(__name__)


class CartListAPIView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user)
        if not cart.exists():
            # Create an empty cart if none exists
            cart = Cart.objects.create(user=self.request.user)
            return [cart]
        return cart


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    if not product_id:
        return Response(
            {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    product = get_object_or_404(Product, id=product_id)

    # Validate stock
    if quantity > product.stock:
        return Response(
            {"error": f"Only {product.stock} items available in stock"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get or create cart for user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Check if item already exists in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # Validate total quantity
        if cart_item.quantity + quantity > product.stock:
            return Response(
                {
                    "error": f"Cannot add {quantity} more items. Only {product.stock - cart_item.quantity} more available"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity
        )

    return Response(
        {"message": "Item added to cart", "cart_total": cart.total_items},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_cart_item(request):
    item_id = request.data.get("item_id")
    quantity = int(request.data.get("quantity", 1))

    if not item_id:
        return Response(
            {"error": "Item ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        cart_item = CartItem.objects.select_related("product").get(
            id=item_id, cart__user=request.user
        )
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Validate stock
    if quantity > cart_item.product.stock:
        return Response(
            {"error": f"Only {cart_item.product.stock} items available in stock"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if quantity < 1:
        cart_item.delete()
        cart = Cart.objects.get(user=request.user)
        return Response(
            {
                "message": "Item removed from cart",
                "cart_total": cart.total_items,
                "cart_total_price": cart.total_price,
            }
        )

    cart_item.quantity = quantity
    cart_item.save()

    return Response(
        {
            "message": "Quantity updated",
            "item_subtotal": cart_item.subtotal,
            "cart_total": cart_item.cart.total_items,
            "cart_total_price": cart_item.cart.total_price,
        }
    )


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "cart/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.prefetch_related("items__product").get(
                user=self.request.user
            )

            if cart.items.count() == 0:
                context["cart"] = None
                return context

            # Get user's addresses
            addresses = self.request.user.addresses.all()

            context.update(
                {
                    "cart": cart,
                    "cart_items": cart.items.all(),
                    "total_price": cart.total_price,
                    "total_items": cart.total_items,
                    "delivery_charge": 50,
                    "grand_total": cart.total_price + 50,
                    "addresses": addresses,
                }
            )
        except Cart.DoesNotExist:
            context["cart"] = None

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        return super().get(request, *args, **kwargs)


def generate_order_number():
    """Generate a unique order number"""
    return get_random_string(length=10, allowed_chars="0123456789")


def create_order_from_cart(request, address_id, payment_method="cash_on_delivery"):
    """Create a new order from cart items"""
    try:
        # Get cart
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related("product").all()

        if not cart_items:
            messages.error(request, "Your cart is empty")
            logger.error("Cart is empty")
            return None

        # Calculate totals
        total_amount = sum(item.subtotal for item in cart_items)
        delivery_charge = 50.00

        # Create order
        order = Order.objects.create(
            user=request.user,
            address_id=address_id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            delivery_charge=delivery_charge,
            payment_method=payment_method,
        )

        # Create order items
        order_items = []
        for cart_item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.selling_price,
                )
            )

        # Bulk create order items
        OrderItem.objects.bulk_create(order_items)

        # Clear cart
        cart.items.all().delete()

        logger.info("Order placed successfully")
        messages.success(request, "Order placed successfully!")
        return order

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found")
        logger.error("Cart not found")
        return None
    except Exception as e:
        messages.error(request, f"Error placing order: {str(e)}")
        logger.error(f"Error placing order: {str(e)}")
        return None


@login_required
def checkout(request):
    """Handle checkout process"""
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        payment_method = request.POST.get("payment_method", "cash_on_delivery")

        if not address_id:
            messages.error(request, "Please select a delivery address")
            return redirect("cart:checkout")

        order = create_order_from_cart(request, address_id, payment_method)
        if order:
            # Redirect to order success page
            return redirect("orders:success", order_number=order.order_number)

        return redirect("cart:checkout")

    # Get user's addresses and cart items for the template
    context = {
        "addresses": Address.objects.filter(user=request.user),
        "cart_items": CartItem.objects.filter(cart__user=request.user).select_related(
            "product"
        ),
    }
    return render(request, "cart/checkout.html", context)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    """Handle order placement"""
    try:
        data = request.data
        address_id = data.get("address_id")
        payment_method = data.get("payment_method", "cash_on_delivery")

        if not address_id:
            return Response(
                {"error": "Please select a delivery address"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = create_order_from_cart(request, address_id, payment_method)
        if order:
            return Response(
                {
                    "message": "Order placed successfully",
                    "redirect_url": reverse(
                        "orders:success", kwargs={"order_number": order.order_number}
                    ),
                }
            )

        return Response(
            {"error": "Error placing order"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
