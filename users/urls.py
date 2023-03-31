from django.urls import path

from .views import UsersAPI

urlpatterns = [
    path("signup", UsersAPI.as_view(http_method_names=["post"])),
    path("signin", UsersAPI.as_view(http_method_names=["get"])),
]
