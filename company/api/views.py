from rest_framework.viewsets import (
    ViewSet,
    ModelViewSet,
    GenericViewSet,
)

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    #IsAdminUser,
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
    IsAdminUser,
    IsOrderOwnerOrReadOnly,
)

from .serializers import (
    CompanySerializer,
    CategorySerializer,
    SubcategorySerializer,
    SubcategoryCreateSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    CartItemSerializer,
    CartItemCreateSerializer,
    WishlistItemSerializer,
    WishlistItemCreateSerializer,
    OrderSerializer,
    OrderCreateSerializer,
)

from django.shortcuts import get_object_or_404

# company views

class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = User.objects.filter(is_company=True)
    permission_classes = [IsOwnerOrReadOnly]

# category views

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


#subcategory views

class SubcategoryViewSet(ModelViewSet):
    queryset = Subcategory.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        context = super().get_serializer_context()
        action = self.action
        if action == "list" or action == "retrieve":
            return SubcategorySerializer
        return SubcategoryCreateSerializer


# product views

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsCompany, IsProductOwnerOrReadOnly]

    def get_serializer_class(self):
        context = super().get_serializer_context()
        action = self.action
        if action == "list" or action == "retrieve":
            return ProductSerializer
        return ProductCreateSerializer

# cart item views 


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsCustomer, IsCartOwnerOrReadOnly]

    def get_serializer_class(self):
        context = super().get_serializer_context()
        action = self.action
        if action == "list" or action == "retrieve":
            return CartItemSerializer
        return CartItemCreateSerializer
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_customer:
            queryset = CartItem.objects.filter(cart__user=self.request.user,is_ordered=False).order_by('-id')
        else:
            queryset = CartItem.objects.filter(is_ordered=False).order_by('-id')
        return queryset

# wishlist views 
   
class WishlistItemViewSet(ModelViewSet):
    permission_classes = [IsCustomer, IsWishlistOwnerOrReadOnly]

    def get_serializer_class(self):
        context = super().get_serializer_context()
        action = self.action
        if action == "list" or action == "retrieve":
            return WishlistItemSerializer
        return WishlistItemCreateSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = WishlistItem.objects.all().order_by('-id')
        return queryset


# order views 

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    permission_classes = [IsCustomer, IsOrderOwnerOrReadOnly]
    
    def get_serializer_class(self):
        context = super().get_serializer_context()
        action = self.action
        if action == "list" or action == "retrieve":
            return OrderSerializer
        return OrderCreateSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.all().order_by("-pk")
        return queryset
    
    def perform_create(self, serializer):
        data = self.request.data
        order = CartItem.objects.get(id=data['order'])
        if Product.objects.get(id=order.product.id).in_stock < CartItem.objects.get(id=data['order']).quantity:
            return
        else:
            serializer.save()
            
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = self.request.data
        order = CartItem.objects.get(id=data['order'])
        message = "out of stock"
        
        if Order.objects.last().order == order:
            message = "order placed"
            
        return Response({
                'message': message,
                'data': response.data
            })
