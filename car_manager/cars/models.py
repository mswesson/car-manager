from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class Car(models.Model):
    """
    ## Модель автомобиля

    Хранит в себе информацию:
    - make (марка автомобиля)
    - model (модель автомобиля)
    - year (год выпуска)
    - description (описание автомобиля)
    - created_at (дата и время создания записи)
    - updated_at (дата и время последнего обновления записи)
    - owner (внешний ключ на пользователя, который создал запись)
    """

    make = models.CharField(max_length=20, null=False, blank=False)
    model = models.CharField(max_length=20, null=False, blank=False)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(timezone.now().year),
        ],
    )
    description = models.TextField(
        max_length=2000, null=True, blank=True, default=""
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cars"
    )

    def description_short(self):
        if len(self.description) <= 155:
            return self.description
        return self.description[:155] + "..."


class CarComment(models.Model):
    """
    ## Модель комментария к автомобилю

    Хранит в себе информацию:
    - content (содержание комментария)
    - created_at (дата и время создания комментария)
    - car (внешний ключ на автомобиль)
    - author (внешний ключ на пользователя)
    """

    content = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=True
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
