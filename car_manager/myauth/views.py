from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    CreateView,
)

from .forms import UserRegistrationForm


class AuthRegisterView(CreateView):
    model = User
    template_name = "auth/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cars:cars_list")


class AuthLoginView(LoginView):
    template_name = "auth/login.html"

    def get_success_url(self):
        return reverse_lazy("cars:cars_list")


class AuthLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")
