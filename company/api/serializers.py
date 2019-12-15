from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    ImageField,
    IntegerField,
    FloatField,
    SerializerMethodField,
)
from customer.models import (
    User,
    Cart,
    Wishlist,
)
from company.models import (
    Category,
    Subcategory,
    Product,
    CartItem,
    WishlistItem,
    Order
)

from rest_framework.response import Response


class CompanySerializer(ModelSerializer):
    name = CharField(source='first_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'profile_images',
        ]


class CompanyUserCreateSerializer(ModelSerializer):
    name = CharField(source='first_name')

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
            'profile_images',
        ]

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        if validated_data['profile_images'] == None:
            del validated_data['profile_images']
        return User.objects.create_user(**validated_data)


class CompanyChangePasswordSerializer(Serializer):
    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password',
        ]
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class CompanyUpdateSerializer(ModelSerializer):
    name = CharField(source='first_name')

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'profile_images',
        ]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class SubcategorySerializer(ModelSerializer):
    category = CharField(source='category.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = [
            'id',
            'name',
            'category',
        ]


class SubcategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = [
            'name',
            'category',
        ]


class ProductSerializer(ModelSerializer):
    category = CharField(source='subcategory.category.name', read_only=True)
    company = CharField(source='company.first_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'company',
            'rate',
            'subcategory',
            'category',
            'description',
            'in_stock',
            'product_image',
            'slug',
        ]


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'rate',
            'subcategory',
            'description',
            'in_stock',
            'product_image',
        ]

    def create(self, validated_data):
        if validated_data['product_image'] == None:
            validated_data.pop('product_image', None)
        print(type(validated_data))
        item = Product.objects.create(**validated_data)
        return item


class CartItemSerializer(ModelSerializer):
    product = CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity',
            'cost',
        ]


class CartItemCreateSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'product',
            'quantity',
        ]


class WishlistItemSerializer(ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = [
            'id',
            'product',
        ]

    def create(self, validated_data):
        print(validated_data)
        item, created = WishlistItem.objects.get_or_create(
            product=validated_data['product'], wishlist=Wishlist.objects.get(user=self.context['request'].user))
        return item


class OrderSerializer(ModelSerializer):
    quantity = CharField(
        source='order.product.quantity', read_only=True)
    cost = CharField(source='order.cost', read_only=True)
    id = IntegerField(source='pk', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order',
            'quantity',
            'cost',
        ]

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['order'].queryset = CartItem.objects.filter(
            cart__user=request_user, is_ordered=False)
