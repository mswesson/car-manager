from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from cars.models import Car, CarComment


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="The password must comply with security requirements",
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CarsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "year"]


class CarsDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            "id",
            "make",
            "model",
            "year",
            "description",
            "created_at",
            "updated_at",
            "owner",
        ]

    def get_owner(self, obj):
        owner = obj.owner.username
        return owner


class CarsCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            "id",
            "make",
            "model",
            "year",
            "description",
            "created_at",
            "updated_at",
            "owner",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]

    def get_owner(self, obj):
        owner = obj.owner.username
        return owner

    def create(self, validated_data):
        owner = self.context["request"].user
        validated_data["owner"] = owner
        return super().create(validated_data)


class CarsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "make",
            "model",
            "year",
            "description",
        ]


class CarsCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ["id", "comments"]

    def get_comments(self, obj):
        comments = CarComment.objects.filter(car=obj).all()
        comments = [
            {
                "author": comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at,
            }
            for comment in comments
        ]
        return comments


class CarsCommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarComment
        fields = ["id", "content", "created_at", "car", "author"]

        read_only_fields = ["id", "created_at", "car", "author"]

    def create(self, validated_data):
        author = self.context["author"]
        car = self.context["car"]
        validated_data["author"] = author
        validated_data["car"] = car
        return super().create(validated_data)
