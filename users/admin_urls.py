from django.urls import path
from users.views.admin_views import (
    admin_dashboard,
    admin_orders,
    admin_order_detail,
    admin_order_edit,
    admin_categories,
    admin_category_add,
    admin_category_edit,
)

urlpatterns = [
    path("", admin_dashboard, name="admin.index"),
    path("orders/", admin_orders, name="admin.orders"),
    path("orders/<int:order_id>/", admin_order_detail, name="admin.order_detail"),
    path("orders/<int:order_id>/edit/", admin_order_edit, name="admin.order_edit"),
    
    path('admin/categories/', admin_categories, name='admin_categories'),
    path('admin/categories/add/', admin_category_add, name='admin_category_add'),
    path('admin/categories/<int:category_id>/edit/', admin_category_edit, name='admin_category_edit'),
]
