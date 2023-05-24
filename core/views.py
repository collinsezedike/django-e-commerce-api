from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import User
from .serializers import UserSerializer


# Create your views here.
@api_view(["GET", "POST"])
def get_and_create_users(request):
    # POST REQUEST
    if request.method == "POST":
        new_user = UserSerializer(data=request.data)
        if new_user.is_valid():
            new_user.save()
            return Response(new_user.data, status=status.HTTP_201_CREATED)
        error_msg = {
            # get only the first error messge
            "error": {next(iter(new_user.errors)): next(iter(new_user.errors.values()))[0]}
        }
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

    # GET REQUEST
    all_users = User.objects.all()
    serialized_users = UserSerializer(all_users, many=True)
    users = {"users": serialized_users.data}
    return Response(users, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def read_update_and_delete_user_by_id(request, id):
    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)

        # PUT REQUEST
        if request.method == "PUT":
            serialized_user = UserSerializer(
                instance=user, data=request.data, partial=True)
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(serialized_user.data, status=status.HTTP_200_OK)
            error_msg = {
                "error": {next(iter(serialized_user.errors)): next(iter(serialized_user.errors.values()))[0]}
            }
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        # DELETE REQUEST
        if request.method == "DELETE":
            user.delete()
            success_msg = { "success": f"User with id '{id}' deleted successfully" }
            return Response(success_msg, status=status.HTTP_204_NO_CONTENT)

        # GET REQUEST
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    else:
        error_msg = { "error": f"User with id '{id}' does not exist" }
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)
    if user is not None:
        token = Token.objects.get_or_creat
        if token.is_valid():
            token.save()
            return Response(token.data, status=status.HTTP_401_UNAUTHORIZED)
        error_msg = { "error": {next(iter(token.errors)): next(iter(token.errors.values()))[0]} }
        return Response(error_msg, status=status.HTTP_401_UNAUTHORIZED)
    error_msg = { "error": "Invalid email address or password" }
    return Response(error_msg, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    print(request.user)
    tokenExists = Token.objects.filter(user=request.user)
    if tokenExists:
        token = Token.objects.get(user=request.user)
        token.delete()
        success_msg = { "success": "Logged user out successfully"}
        return Response(success_msg, status=status.HTTP_200_OK)
    error_msg = { "error": "User is not authenticated"}
    return Response(error_msg, status=status.HTTP_200_OK)