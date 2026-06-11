from rest_framework import serializers
from .models import User

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "age"]
        extra_kwargs = {
            "email": {"required": False},
            "age": {"required": False},
        }

    def to_internal_value(self, data):
        allowed_fields = set(self.fields.keys())
        provided_fields = set(data.keys())

        extra_fields = provided_fields - allowed_fields
        if extra_fields:
            raise serializers.ValidationError({
                field: "This field is not allowed."
                for field in extra_fields
            })

        return super().to_internal_value(data)