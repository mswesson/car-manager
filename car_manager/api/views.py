from django.contrib.auth import authenticate
from django.test import Client as RequestsClient
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserCreateSerializer,
    CarsListSerializer,
    CarsDetailSerializer,
    CarsCommentsSerializer,
    CarsCreateSerializer,
    CarsUpdateSerializer,
    CarsCommentsCreateSerializer,
)
from cars.models import Car


class UserCreateApiView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        """Регистрация"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        password = request.data.get("password")

        request_client = RequestsClient()
        response = request_client.post(
            path=reverse_lazy("api:token"),
            data={"username": user.username, "password": password},
            content_type="application/json",
        )
        data = {
            "username": user.username,
            "token": response.data.get("access"),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        """Логин"""
        user_data = request.data
        username = user_data["username"]
        password = user_data["password"]

        user = authenticate(request, username=username, password=password)

        if not user:
            data = {"error": "User not found"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        request_client = RequestsClient()
        response = request_client.post(
            path=reverse_lazy("api:token"),
            data={"username": username, "password": password},
            content_type="application/json",
        )
        data = {
            "username": user.username,
            "token": response.data.get("access"),
        }
        return Response(data, status=status.HTTP_200_OK)


class CarListApiView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request: Request, *args, **kwargs):
        """Список автомобилей"""
        cars = Car.objects.all()
        serializer = CarsListSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        """Создание автомобиля"""
        serializer = CarsCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CarDetailApiView(CarListApiView):
    http_method_names = ["get", "put", "delete"]

    def get(self, request: Request, *args, **kwargs):
        """Информация об автомобиле"""
        car = Car.objects.filter(pk=self.kwargs.get("pk")).first()

        if not car:
            return self.car_not_found()

        serializer = CarsDetailSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        """Обновление автомобиля"""
        car = Car.objects.filter(pk=self.kwargs.get("pk")).first()

        if car.owner != request.user:
            return self.access_denied()

        if not car:
            return self.car_not_found()

        serializer = CarsUpdateSerializer(instance=car, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_car = serializer.save()

        return Response(
            CarsUpdateSerializer(updated_car).data, status=status.HTTP_200_OK
        )

    def delete(self, request: Request, *args, **kwargs):
        """Удаление автомобиля"""
        car = Car.objects.filter(pk=self.kwargs.get("pk")).first()

        if car.owner != request.user:
            return self.access_denied()

        if not car:
            return self.car_not_found()

        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def car_not_found(self):
        """водит ошибку, что автомобиль не найден"""
        return Response(
            {"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def access_denied(self):
        return Response(
            {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
        )


class CarCommentsApiView(CarDetailApiView):
    http_method_names = ["get", "post"]

    def get(self, request: Request, *args, **kwargs):
        """Комментарии об автомобиле"""
        car = Car.objects.filter(pk=self.kwargs.get("pk")).first()

        if not car:
            return self.car_not_found()

        serializer = CarsCommentsSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        """Создание комментария"""
        author = request.user
        car = Car.objects.filter(pk=self.kwargs.get("pk")).first()

        if not car:
            return self.car_not_found()

        context = {
            "author": author,
            "car": car,
        }
        serializer = CarsCommentsCreateSerializer(
            data=request.data, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
