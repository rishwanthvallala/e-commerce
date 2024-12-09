from django.urls import path
from .views import UserLoginView, UserSignupView, forgot_password, logout_view, add_address
from django.views.decorators.http import require_http_methods

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('logout/', require_http_methods(['POST'])(logout_view), name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('api/address/add/', add_address, name='add_address'),
]
