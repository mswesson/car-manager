from django.contrib import admin
from .models import Car, CarComment


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "make",
        "model",
        "year",
        "description",
        "owner",
        "created_at",
        "updated_at",
    )
    fields = ("make", "model", "year", "description", "owner")


@admin.register(CarComment)
class CarCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "created_at", "car", "author")
    fields = ("content", "car", "author")
