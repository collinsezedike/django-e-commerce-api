from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from customers.models import CustomerProfile
from products.models import Product

from .models import Cart, CartItem
from .serializers import CartItemSerializer


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def read_cart(request):
    user = CustomerProfile.objects.get(user=request.user)
    user_cart = Cart.objects.get_or_create(user=user)[0]
    all_cart_items = CartItem.objects.filter(cart=user_cart)
    serialized_cart_items = CartItemSerializer(all_cart_items, many=True)
    return Response(serialized_cart_items.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    if not request.data.get("product"):
        error_msg = { "error": "required product id is missing" }
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
    
    user = CustomerProfile.objects.get(user=request.user)
    user_cart = Cart.objects.get_or_create(user=user)[0]
    product_to_add = Product.objects.get(id=request.data.get("product"))
    new_cart_item, isCreated = CartItem.objects.get_or_create(cart=user_cart, item=product_to_add)

    if not isCreated:
        if request.data.get("quantity"):
            if not request.data["quantity"].isdecimal() or int(request.data["quantity"]) <= 0:
                error_msg = { "error": "cart item quantity must be a positive integer" }
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_cart_item.quantity = request.data.get("quantity")
        else:
            new_cart_item.quantity += 1
        new_cart_item.save()

    all_cart_items = CartItem.objects.filter(cart=user_cart)
    serialized_cart_items = CartItemSerializer(all_cart_items, many=True)
    return Response(serialized_cart_items.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    if not request.data.get("product"):
        error_msg = { "error": "required product id is missing" }
        return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
    
    user = CustomerProfile.objects.get(user=request.user)
    user_cart = Cart.objects.get(user=user)
    product_to_remove = Product.objects.get(id=request.data.get("product"))

    if CartItem.objects.filter(cart=user_cart, item=product_to_remove).exists():
        error_msg = { "error": "Cart item does not exist" }
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
    else:
        cart_item_to_remove = CartItem.objects.get(cart=user_cart, item=product_to_remove)

    if request.data.get("quantity"):
        if not request.data["quantity"].isdecimal() or int(request.data["quantity"]) < 0:
            error_msg = { "error": "cart item quantity must be a positve integer" }
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        elif int(request.data.get("quantity")) == 0:
            cart_item_to_remove.delete()
        else:
            cart_item_to_remove.quantity = request.data.get("quantity")
    else:
        cart_item_to_remove.quantity -= 1

    if cart_item_to_remove.quantity <= 0:
        cart_item_to_remove.delete()
    else:
        cart_item_to_remove.save()

    all_cart_items = CartItem.objects.filter(cart=user_cart)
    serialized_cart_items = CartItemSerializer(all_cart_items, many=True)
    return Response(serialized_cart_items.data, status=status.HTTP_200_OK)
