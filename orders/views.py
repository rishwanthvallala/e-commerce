from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from users.models import Address


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/success.html", {"order": order})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Check if order can be cancelled
        if order.status != Order.StatusChoices.PENDING:
            return Response({
                'error': 'Only pending orders can be cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update order status
        order.status = Order.StatusChoices.CANCELLED
        order.save()
        
        return Response({
            'message': 'Order cancelled successfully'
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@login_required
def place_order(request):
    if request.method == "POST":
        # Get selected addresses from form
        shipping_address_id = request.POST.get('shipping_address')
        billing_address_id = request.POST.get('billing_address')
        
        # Get addresses from database
        shipping_address = Address.objects.get(id=shipping_address_id, user=request.user)
        billing_address = None
        if billing_address_id:
            billing_address = Address.objects.get(id=billing_address_id, user=request.user)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            billing_address=billing_address or shipping_address,  # Use shipping address if no billing address
            order_number=generate_order_number(),  # You'll need to implement this
            total_amount=calculate_total(request.user.cart),  # You'll need to implement this
            payment_method=request.POST.get('payment_method', 'cash_on_delivery'),
            notes=request.POST.get('notes', '')
        )

        # Create order items from cart
        for cart_item in request.user.cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear cart
        request.user.cart.items.all().delete()

        return redirect('orders:order_success', order_id=order.id)

    # GET request - show order form
    context = {
        'addresses': request.user.addresses.all(),
        'cart_total': request.user.cart.get_total(),
        'delivery_charge': 50.00,  # You might want to calculate this dynamically
    }
    return render(request, 'orders/checkout.html', context)
