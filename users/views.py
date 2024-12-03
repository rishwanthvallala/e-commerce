from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginView(LoginView):
    template_name = "users/auth/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:home")


class UserSignupView(CreateView):
    template_name = "users/auth/signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")

    def form_invalid(self, form):
        # This will return the form with errors to the template
        print("Form errors:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        print(response)
        return response


def forgot_password(request):
    return render(request, "users/auth/forgot-password.html")
