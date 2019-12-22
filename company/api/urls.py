from django.urls import path

from .views import (
    CompanyViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    ProductViewSet,
    CartItemViewSet,
    WishlistItemViewSet,
    OrderViewSet,
)

from rest_framework.routers import DefaultRouter

app_name = 'Companyapi'

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubcategoryViewSet, basename='subcategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'wishlist', WishlistItemViewSet, basename='wishlist')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = router.urls
