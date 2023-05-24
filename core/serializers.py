from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "type",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, request_data):
        """
        Checks if password and password2 match only when creating a new user
        """
        if (
            self.instance is None
            and request_data["password"] != request_data["password2"]
        ):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return request_data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            type=validated_data.get("type", "customer"),
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        valid_updatable_fields = ["first_name", "last_name", "type"]
        # decided to use this instead of hasattr() because
        # if a user can guess the attribute names,
        # the dataabase is in trouble
        for field in validated_data:
            if field in valid_updatable_fields:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance

## This would be the user validator component.
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(style={"input_type": "password"})

#     def validate(self, attrs):
#         email = attrs.get("email")
#         password = attrs.get("password")

#         if email and password:
#             print(email, password)
#             user = authenticate(email=email, password=password)
#             if user:
#                 if not user.is_active:
#                     msg = _("User account is disabled.")
#                     raise serializers.ValidationError(msg)
#             else:
#                 msg = _("Invalid Email address or password")
#                 raise serializers.ValidationError(msg)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise serializers.ValidationError(msg)

#         attrs["user"] = user
        # return attrs

