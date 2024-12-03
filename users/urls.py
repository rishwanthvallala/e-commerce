from django.urls import path
from .views import UserLoginView, UserSignupView, forgot_password
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
]
