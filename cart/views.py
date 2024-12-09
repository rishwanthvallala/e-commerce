from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer


class CartListAPIView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddToCartAPIView(APIView):
    def post(self, request):
        cart = Cart.objects.create(user=request.user)
        return Response({"message": "Cart created"}, status=201)


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
