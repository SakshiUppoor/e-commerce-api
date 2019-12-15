from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    GenericAPIView,
)

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
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
    Order,
)

from.permissions import (
    IsProductOwnerOrReadOnly,
    IsOwnerOrReadOnly,
    IsCompany,
    IsCustomer,
    IsCartOwnerOrReadOnly,
    IsWishlistOwnerOrReadOnly,
    IsCartOwner,
)

from .serializers import (
    CompanySerializer,
    CompanyUserCreateSerializer,
    CompanyUpdateSerializer,
    CompanyChangePasswordSerializer,
    CategorySerializer,
    SubcategorySerializer,
    SubcategoryCreateSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    CartItemSerializer,
    CartItemCreateSerializer,
    WishlistItemSerializer,
    OrderSerializer,
)


# company views

class CompanyListAPIView(ListAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = CompanySerializer

class CompanyDetailAPIView(RetrieveAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = CompanySerializer

class CompanyCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CompanyUserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer, **kwargs):
        serializer.save(is_company=True)

class CompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = CompanyUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    model = User

class CompanyChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = CompanyChangePasswordSerializer
    permission_classes = [IsOwnerOrReadOnly]
    model = User

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                response = {
                    'message': 'Old password is wrong.',
                }

                return Response(response)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors)

class CompanyDeleteAPIView(DestroyAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


# category views

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 
class CategoryCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser,]
    #authentication_classes = [TokenAuthentication,]

class CategoryUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    model = User

class CategoryDeleteAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


#subcategory views

class SubcategoryListAPIView(ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class SubcategoryDetailAPIView(RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class SubcategoryCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SubcategoryCreateSerializer
    permission_classes = [IsAdminUser]

class SubcategoryUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryCreateSerializer
    permission_classes = [IsAdminUser]
    model = User

class SubcategoryDeleteAPIView(DestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminUser]


# product views

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsCompany]
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

class ProductUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsProductOwnerOrReadOnly]
    model = User

class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductOwnerOrReadOnly]


# cart item views 

class CartItemListAPIView(ListAPIView):
    serializer_class = CartItemSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = CartItem.objects.filter(cart__user=self.request.user,is_ordered=False).order_by('-id')
        return queryset

class CartItemDetailAPIView(RetrieveAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = CartItem.objects.filter(cart__user=self.request.user,is_ordered=False).order_by('-id')
        return queryset

class CartItemCreateAPIView(CreateAPIView):
    queryset = CartItem.objects.filter(is_ordered=False)
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsCustomer]
    
    def perform_create(self, serializer):
        if Cart.objects.filter(user=self.request.user).exists():
            serializer.save(cart=Cart.objects.get(user=self.request.user))

class CartItemUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsCartOwner]
    model = CartItem
    
    def get_queryset(self, *args, **kwargs):
        queryset = CartItem.objects.filter(cart__user=self.request.user,is_ordered=False).order_by('-id')
        return queryset

class CartItemDeleteAPIView(DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsCartOwner]

    def get_queryset(self, *args, **kwargs):
        queryset = CartItem.objects.filter(cart__user=self.request.user,is_ordered=False).order_by('-id')
        return queryset


# wishlist views 
   
class WishlistItemCreateAPIView(CreateAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsCustomer]
    
    def get_queryset(self, *args, **kwargs):
        queryset = WishlistItem.objects.filter(wishlist__user=self.request.user,is_ordered=False).order_by('-id')
        return queryset
    
class WishlistItemDeleteAPIView(DestroyAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsWishlistOwnerOrReadOnly]
    
    def get_queryset(self, *args, **kwargs):
        queryset = WishlistItem.objects.filter(wishlist__user=self.request.user,is_ordered=False).order_by('-id')
        return queryset


# order views 

class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.filter(order__cart__user=self.request.user)
        return queryset

class OrderDetailAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.filter(order__cart__user=self.request.user)
        return queryset

class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.filter(order__cart__user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        data = self.request.data
        order = CartItem.objects.get(id=data['order'])
        if Product.objects.get(id=order.product.id).in_stock == 0:
            return Response({'message':'Out Of Stock'})
        else:
            serializer.save()

    '''def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            product = serializer.data.get("product")
            product.is_ordered = True
            product.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)'''
