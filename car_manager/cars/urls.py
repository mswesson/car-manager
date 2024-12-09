from django.urls import path

from .views import (
    CarsListView,
    CarsCreateView,
    CarsDetailView,
    CarsUpdateView,
    CarsDeleteView,
    CarCommentCreateView,
    CarCommentDeleteView,
    CarCommentsUpdateView,
)

app_name = "cars"

urlpatterns = [
    path("", CarsListView.as_view(), name="cars_list"),
    path("create/", CarsCreateView.as_view(), name="cars_create"),
    path("<int:pk>/", CarsDetailView.as_view(), name="cars_detail"),
    path("<int:pk>/update/", CarsUpdateView.as_view(), name="cars_update"),
    path("<int:pk>/delete/", CarsDeleteView.as_view(), name="cars_delete"),
    path(
        "<int:pk>/add_comment/",
        CarCommentCreateView.as_view(),
        name="comments_cars_create",
    ),
    path(
        "comment/<int:pk>/delete/",
        CarCommentDeleteView.as_view(),
        name="comments_cars_delete",
    ),
    path(
        "comment/<int:pk>/update/",
        CarCommentsUpdateView.as_view(),
        name="comments_cars_update",
    ),
]
