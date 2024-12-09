from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('categories.urls')),
    path('', include('users.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
]
