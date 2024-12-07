from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginView(FormView):
    template_name = "users/auth/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("core:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        # Pass the invalid form directly to maintain error messages
        return self.render_to_response(self.get_context_data(form=form))


class UserSignupView(CreateView):
    template_name = "users/auth/signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        # This will return the form with errors to the template
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        print(response)
        return response


def forgot_password(request):
    return render(request, "users/auth/forgot-password.html")


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')
    return redirect('core:home')
