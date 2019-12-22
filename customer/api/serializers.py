from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)

from customer.models import User


class CustomerSerializer(ModelSerializer):
    email = EmailField(source='username')
    password = CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'profile_image',
            'password',
        ]

    def create(self, validated_data):
        if 'profile_image' in validated_data and validated_data['profile_image'] == None:
            del validated_data['profile_image']
        return User.objects.create_user(**validated_data, is_customer=True)
