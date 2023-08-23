from rest_framework import serializers
from .models import Greeting

class GreetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Greeting
        fields = (
            "id",
            "text",
            "user",
            "created_at",
            "last_modified_at",
        )
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "last_modified_at",
        )