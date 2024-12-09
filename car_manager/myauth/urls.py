from django.urls import path

from .views import AuthRegisterView, AuthLoginView, AuthLogoutView

app_name = "myauth"

urlpatterns = [
    path("register/", AuthRegisterView.as_view(), name="register"),
    path("logout/", AuthLogoutView.as_view(), name="logout"),
    path("login/", AuthLoginView.as_view(), name="login"),
]
