from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('api/list/', views.CartListAPIView.as_view(), name='api.cart-list'),
    path('api/add/', views.add_to_cart, name='add_to_cart'),
    path('api/update/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
