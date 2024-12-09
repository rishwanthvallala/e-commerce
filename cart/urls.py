from django.urls import path
from .views import CartListAPIView

app_name = "cart"

urlpatterns = [
    path("api/list/", CartListAPIView.as_view(), name="api.cart-list"),
]
