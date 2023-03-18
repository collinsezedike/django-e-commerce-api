from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.decorators import api_view
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
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)

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
            serialized_user = UserSerializer(instance=user, data=request.data, partial=True)
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(serialized_user.data, status=status.HTTP_200_OK)
            return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

        # DELETE REQUEST
        if request.method == "DELETE":
            user.delete()
            success_msg = {
                "success": f"user with id '{id}' deleted successfully"}
            return Response(success_msg, status=status.HTTP_204_NO_CONTENT)

        # GET REQUEST
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    else:
        error_msg = {"error": f"user with id '{id}' does not exist"}
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)
    print(user)
    if user is not None:
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    error_msg = {"error": "invalid email address or password"}
    return Response(error_msg, status=status.HTTP_401_UNAUTHORIZED)