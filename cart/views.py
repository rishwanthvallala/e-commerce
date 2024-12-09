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

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    
    if not product_id:
        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    product = get_object_or_404(Product, id=product_id)
    
    # Validate stock
    if quantity > product.stock:
        return Response(
            {'error': f'Only {product.stock} items available in stock'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get or create cart for user
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Check if item already exists in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # Validate total quantity
        if cart_item.quantity + quantity > product.stock:
            return Response(
                {'error': f'Cannot add {quantity} more items. Only {product.stock - cart_item.quantity} more available'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )
    
    return Response({
        'message': 'Item added to cart',
        'cart_total': cart.total_items
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request):
    item_id = request.data.get('item_id')
    quantity = int(request.data.get('quantity', 1))
    
    if not item_id:
        return Response({'error': 'Item ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        cart_item = CartItem.objects.select_related('product').get(
            id=item_id, 
            cart__user=request.user
        )
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Validate stock
    if quantity > cart_item.product.stock:
        return Response(
            {'error': f'Only {cart_item.product.stock} items available in stock'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if quantity < 1:
        cart_item.delete()
        cart = Cart.objects.get(user=request.user)
        return Response({
            'message': 'Item removed from cart',
            'cart_total': cart.total_items,
            'cart_total_price': cart.total_price
        })
    
    cart_item.quantity = quantity
    cart_item.save()
    
    return Response({
        'message': 'Quantity updated',
        'item_subtotal': cart_item.subtotal,
        'cart_total': cart_item.cart.total_items,
        'cart_total_price': cart_item.cart.total_price
    })


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.prefetch_related(
                'items__product'
            ).get(user=self.request.user)
            
            if cart.items.count() == 0:
                context['cart'] = None
                return context
            
            # Get user's addresses
            addresses = self.request.user.addresses.all()
            
            context.update({
                'cart': cart,
                'cart_items': cart.items.all(),
                'total_price': cart.total_price,
                'total_items': cart.total_items,
                'delivery_charge': 50,
                'grand_total': cart.total_price + 50,
                'addresses': addresses
            })
        except Cart.DoesNotExist:
            context['cart'] = None
            
        return context
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return super().get(request, *args, **kwargs)
