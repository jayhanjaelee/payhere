from rest_framework import serializers
from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    def get_user_by_email(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None
