from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ImageField,
    Serializer
)

from customer.models import User


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomerCreateSerializer(ModelSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    password = CharField(write_only=True)
    email = EmailField(source='username')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'profile_image',
        ]

    def create(self, validated_data):
        user = super(CustomerCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerChangePasswordSerializer(Serializer):
    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password',
        ]
    """
    Serializer for password change endpoint.
    """
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class CustomerUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_image'
        ]
