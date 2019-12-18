from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    ImageField,
    IntegerField,
    ModelField,
    FloatField,
    PrimaryKeyRelatedField,
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
            'profile_image',
        ]


class CompanyUserCreateSerializer(ModelSerializer):
    name = CharField(source='first_name')
    email = EmailField(source='username')

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
            'profile_image',
        ]

    def create(self, validated_data):
        """
        If profile image is not provided, 
        removing the field from the dictionary,
        so that default image is used.
        """
        if 'profile_image' in validated_data and validated_data['profile_image'] == None:
            del validated_data['profile_image']
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
            'profile_image',
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
    name = CharField(required=True)
    category = PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=True)

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
    rate = FloatField(required=True)
    name = CharField(required=True)
    subcategory = PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all(), required=True)
    in_stock = IntegerField(required=True)

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
        """
        If product image is not provided, 
        removing the field from the dictionary,
        so that default image is used.
        """
        if 'product_image' in validated_data and validated_data['product_image'] == None:
            validated_data.pop('product_image', None)
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
    quantity = IntegerField(required=True)

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
        """
        Creating wishlistitem only if it
        doesn't already exist in the user's list.
        """
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
        """
        Filter for the order field.
        Customers can only order from their cart items.
        """
        super(OrderSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['order'].queryset = CartItem.objects.filter(
            cart__user=request_user, is_ordered=False)

    def create(self, validated_data):
        product = validated_data['order'].product
        item = Order.objects.create(**validated_data)
        return item
