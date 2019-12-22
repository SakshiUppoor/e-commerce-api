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

from customer.api.serializers import CustomerSerializer

from company.models import (
    Category,
    Subcategory,
    Product,
    CartItem,
    WishlistItem,
    Order,
)

from rest_framework.response import Response
from rest_framework.validators import UniqueValidator


class CompanySerializer(ModelSerializer):
    required = True
    name = CharField(source='first_name')
    email = EmailField(source='username', validators=[
                       UniqueValidator(queryset=User.objects.all())])
    password = CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'profile_image',
            'password',
        ]

    def create(self, validated_data):
        """
        If profile image is not provided, 
        removing the field from the dictionary,
        so that default image is used.
        """
        if 'profile_image' in validated_data and validated_data['profile_image'] == None:
            del validated_data['profile_image']
        return User.objects.create_user(**validated_data, is_company=True)


class CategorySerializer(ModelSerializer):
    name = CharField(validators=[
        UniqueValidator(queryset=Category.objects.all())])

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class SubcategorySerializer(ModelSerializer):
    required = True
    category = CategorySerializer(many=False,)

    class Meta:
        model = Subcategory
        exclude = []


class SubcategoryCreateSerializer(ModelSerializer):
    required = True

    class Meta:
        model = Subcategory
        exclude = []


class ProductSerializer(ModelSerializer):
    subcategory = SubcategorySerializer(many=False,)
    company = CompanySerializer(many=False,)

    class Meta:
        model = Product
        exclude = []


class ProductCreateSerializer(ModelSerializer):
    required = True

    class Meta:
        model = Product
        exclude = ['slug', 'company']

    def create(self, validated_data):
        """
        If product image is not provided, 
        removing the field from the dictionary,
        so that default image is used.
        """
        if 'product_image' in validated_data and validated_data['product_image'] == None:
            validated_data.pop('product_image', None)
        company = self.context['request'].user
        item = Product.objects.create(**validated_data, company=company)
        return item


class CartSerializer(ModelSerializer):
    user = CustomerSerializer(many=False,)

    class Meta:
        model = Cart
        exclude = []


class CartItemSerializer(ModelSerializer):
    product = ProductSerializer(many=False,)
    cart = CartSerializer(many=False,)

    class Meta:
        model = CartItem
        exclude = ['is_ordered']


class CartItemCreateSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        cart = Cart.objects.get(user=self.context['request'].user)
        return CartItem.objects.create(cart=cart, **validated_data)


class WishlistSerializer(ModelSerializer):
    user = CustomerSerializer(many=False,)

    class Meta:
        model = Wishlist
        exclude = []


class WishlistItemSerializer(ModelSerializer):
    product = ProductSerializer(many=False,)
    wishlist = WishlistSerializer()

    class Meta:
        model = WishlistItem
        exclude = []


class WishlistItemCreateSerializer(ModelSerializer):
    class Meta:
        model = WishlistItem
        exclude = ['wishlist']

    def create(self, validated_data):
        """
        Creating wishlistitem only if it
        doesn't already exist in the user's list.
        """
        item, created = WishlistItem.objects.get_or_create(
            product=validated_data['product'], wishlist=Wishlist.objects.get(user=self.context['request'].user))
        return item


class OrderSerializer(ModelSerializer):
    order = CartItemSerializer(many=False,)

    class Meta:
        model = Order
        exclude = []


class OrderCreateSerializer(ModelSerializer):
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
        super(OrderCreateSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['order'].queryset = CartItem.objects.filter(
            cart__user=request_user, is_ordered=False)

    def create(self, validated_data):
        product = validated_data['order'].product
        item = Order.objects.create(**validated_data)
        return item
