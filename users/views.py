import bcrypt

from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import json


@api_view(["GET"])
def index(request):
    api_urls = {
        "signup": "/users/signup",
        "signin": "/users/signin",
    }

    return Response(api_urls)


class UsersAPI(APIView):
    def get(self, request):
        print("signin")
        queryset = User.objects.all()
        print("get queryset: ", queryset)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        request_body = json.loads(request.body.decode("utf-8"))
        email = request_body.get("email")
        password = request_body.get("password")

        if not email or not password:
            return Response(
                {"error": "INVALIED_USER_INPUT."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        encoded_password = encode_password(password)

        user = User(email=email, password=encoded_password)
        user.save()

        return Response(
            {"message": f"{email} IS CREATED."}, status=status.HTTP_201_CREATED
        )

    def get_view_name(self):
        return "Users API"


def encode_password(password):
    salt = bcrypt.gensalt(12)
    encoded_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return encoded_password
