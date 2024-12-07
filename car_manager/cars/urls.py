from django.urls import path, include

from .views import CarsListView, CarsCreateView, CarsDetailView, CarsUpdateView, CarsDeleteView

app_name = "cars"

urlpatterns = [
    path("", CarsListView.as_view(), name="cars_list"),
    path("create/", CarsCreateView.as_view(), name="cars_create"),
    path("<int:pk>/", CarsDetailView.as_view(), name="cars_detail"),
    path("<int:pk>/update/", CarsUpdateView.as_view(), name="cars_update"),
    path("<int:pk>/delete/", CarsDeleteView.as_view(), name="cars_delete"),
]