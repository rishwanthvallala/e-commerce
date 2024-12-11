from django.urls import path
from users.views.admin_views import admin_dashboard

urlpatterns = [
    path("", admin_dashboard, name="admin.index"),
]
