from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('api/add/', views.add_to_cart, name='add_to_cart'),
]
