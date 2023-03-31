from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def index(request):
    api_urls = {
        "signup": "/users/signup",
        "signin": "/users/signin",
    }

    return Response(api_urls, template_name="Payhere API List")
