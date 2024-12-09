from django.urls import path, include
from .views import (
    DashboardView,
    UserLoginView,
    UserSignupView,
    forgot_password,
    logout_view,
    add_address,
    ProfileView,
    OrderListView,
    WishlistView,
    AddressListView,
)
from django.views.decorators.http import require_http_methods

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("logout/", require_http_methods(["POST"])(logout_view), name="logout"),
    path("forgot-password/", forgot_password, name="forgot-password"),
    path("api/address/add/", add_address, name="add_address"),
    path(
        "dashboard/",
        include(
            [
                path("", DashboardView.as_view(), name="dashboard.index"),
                path("profile/", ProfileView.as_view(), name="dashboard.profile"),
                path("orders/", OrderListView.as_view(), name="dashboard.orders"),
                path("wishlist/", WishlistView.as_view(), name="dashboard.wishlist"),
                path("addresses/", AddressListView.as_view(), name="dashboard.addresses"),
            ]
        ),
    ),
]
