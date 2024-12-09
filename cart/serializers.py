from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(method_name="get_items")

    class Meta:
        model = Cart
        fields = "__all__"

    def get_items(self, obj):
        return obj.items.all()
