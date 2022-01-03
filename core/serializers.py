from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import URL

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return f"http://localhost:8000/{obj.code}/"

    class Meta:
        model = URL
        fields = ("id", "url", "short_url", "clicks", "created")
        read_only_fields = ("clicks",)
