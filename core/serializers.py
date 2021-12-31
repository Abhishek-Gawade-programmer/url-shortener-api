from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return f"http://localhost:8000/{obj.code}/"

    class Meta:
        model = URL
        fields = ("id", "url", "short_url", "clicks", "created")
        read_only_fields = ("clicks",)
