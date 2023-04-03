import io
import os
import math
from datetime import datetime, timezone

import jwt
import bcrypt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


from .models import User
from .serializers import UserSignUpSerializer

load_dotenv()


class UsersAPI(APIView):
    def get(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "USER INPUT IS INVALID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)
        password_match = check_password(
            password=password, hashed_password=user.password
        )

        if not password_match:
            return Response({"error": "INVALID_PASSWORD"})

        secret_key = os.getenv("JWT_SECRET_KEY")
        payload = {
            "id": user.id,
            "iat": get_creent_time_in_utc(),
            "exp": get_expired_time_in_utc(),
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return Response({"token": token})

    def post(self, request):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        password = data.get("password")
        if not password:
            return Response(
                {"error": "INVALID_PASSWORD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["password"] = generate_hashed_password(password)
        serializer = UserSignUpSerializer(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            return Response(
                {"error": errors}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        email = serializer.validated_data["email"]
        return Response(
            {"message": f"{email} IS CREATED."},
            status=status.HTTP_201_CREATED,
        )

    def get_view_name(self):
        return "Users API"


def check_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def generate_hashed_password(password):
    salt = bcrypt.gensalt(12)
    encoded_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return encoded_password.decode("utf-8")


def get_creent_time_in_utc():
    utc_time = (datetime.now(timezone.utc).timestamp() + (60 * 60 * 9)) * 1000
    return math.floor(utc_time)


def get_expired_time_in_utc():
    diff = 60 * 60 * 24 * 1000
    return get_creent_time_in_utc() + diff
