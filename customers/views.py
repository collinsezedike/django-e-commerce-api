from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CustomerProfile
from .serializers import CustomerProfileSerializer


@api_view(["GET"])
def get_all_customer_profiles(request):
    all_customer_profiles = CustomerProfile.objects.all()
    serialized_customer_profiles = CustomerProfileSerializer(
        all_customer_profiles, many=True
    )
    customer_profiles = {"customers": serialized_customer_profiles.data}
    return Response(customer_profiles, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def read_update_and_delete_customer_profile_by_id(request, id):
    if CustomerProfile.objects.filter(id=id).exists():
        customer_profile = CustomerProfile.objects.get(id=id)

        # PUT REQUEST
        if request.method == "PUT":
            serialized_customer_profile = CustomerProfileSerializer(
                instance=customer_profile, data=request.data, partial=True
            )
            if serialized_customer_profile.is_valid():
                serialized_customer_profile.save()
                return Response(serialized_customer_profile.data, status=status.HTTP_201_CREATED)
            return Response(serialized_customer_profile.errors, status=status.HTTP_400_BAD_REQUEST)

        # DELETE REQUEST
        if request.method == "DELETE":
            customer_profile.delete()
            success_msg = {"success": f"customer profile with id {id} deleted successfully"}
            return Response(success_msg, status=status.HTTP_204_NO_CONTENT)

        # GET REQUEST
        serialized_customer_profile = CustomerProfileSerializer(customer_profile)
        return Response(serialized_customer_profile.data, status=status.HTTP_200_OK)
    else:
        error_msg = {"error": f"customer profile with id {id} does not exist"}
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
