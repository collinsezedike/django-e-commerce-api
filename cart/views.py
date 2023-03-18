from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
@api_view(["GET"])
def read_cart(request):
    return Response(status=status.HTTP_200_OK)

def add_to_cart(request):
    return Response(status=status.HTTP_200_OK)

def remove_from_cart(request):
    return Response(status=status.HTTP_200_OK)