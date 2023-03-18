from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


@api_view(["GET", "POST"])
def read_and_create_products(request):
    # POST REQUEST
    if request.method == "POST":
        new_product_serializer = ProductSerializer(data=request.data)
        if new_product_serializer.is_valid():
            new_product_serializer.save()
            return Response(new_product_serializer.data, status=status.HTTP_201_CREATED)
        error_msg = {"error": "incomplete or invalid data passed"}
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
    
    # GET REQUEST
    products = Product.objects.all()
    serialized_products = ProductSerializer(products, many=True)
    products = {"products": serialized_products.data}
    return Response(products, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def read_update_and_delete_product_by_id(request, id):
    if Product.objects.filter(id=id).exists():
        product = Product.objects.get(id=id)

        # PUT REQUEST
        if request.method == "PUT":
            serialized_product = ProductSerializer(instance=product, data=request.data, partial=True)
            if serialized_product.is_valid():
                serialized_product.save()
                return Response(serialized_product.data, status=status.HTTP_200_OK)
            return Response(serialized_product.error, status=status.HTTP_400_BAD_REQUEST)

        # DELETE REQUEST
        if request.method == "DELETE":
            product.delete()
            success_msg = {"success": f"product with id {id} deleted successfully"}
            return Response(success_msg, status=status.HTTP_204_NO_CONTENT)

        # GET REQUEST
        serialized_product = ProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    else:
        error_msg = {"error": f"product with id {id} does not exist"}
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def search_product(request):
    suggested_products = Product.objects.filter()   # check name, price and description
    serialized_suggestions = ProductSerializer(suggested_products, many=True)
    return Response(serialized_suggestions, status=status.HTTP_200_OK)