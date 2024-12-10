from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserCreateApiView,
    UserLoginApiView,
    CarCommentsApiView,
    CarDetailApiView,
    CarListApiView,
)

app_name = "api"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path("cars/", CarListApiView.as_view(), name="car_detail"),
    path("cars/<int:pk>/", CarDetailApiView.as_view(), name="cars_detail"),
    path(
        "cars/<int:pk>/comments/",
        CarCommentsApiView.as_view(),
        name="cars_comments",
    ),
]
