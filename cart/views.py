from rest_framework.generics import ListAPIView

from .models import Cart
from .serializers import CartSerializer


class CartListAPIView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
