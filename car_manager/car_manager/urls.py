from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cars/", include("cars.urls")),
    path("auth/", include("myauth.urls")),
    path("api/", include("api.urls")),
]
