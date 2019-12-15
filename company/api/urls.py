from django.urls import path

from .views import (
    CompanyListAPIView,
    CompanyDetailAPIView,
    CompanyCreateAPIView,
    CompanyUpdateAPIView,
    CompanyDeleteAPIView,
    CompanyChangePasswordAPIView,

    CategoryListAPIView,
    CategoryDetailAPIView,
    CategoryCreateAPIView,
    CategoryUpdateAPIView,
    CategoryDeleteAPIView,

    SubcategoryListAPIView,
    SubcategoryDetailAPIView,
    SubcategoryCreateAPIView,
    SubcategoryUpdateAPIView,
    SubcategoryDeleteAPIView,

    ProductListAPIView,
    ProductDetailAPIView,
    ProductCreateAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,

    CartItemListAPIView,
    CartItemDetailAPIView,
    CartItemCreateAPIView,
    CartItemUpdateAPIView,
    CartItemDeleteAPIView,

    OrderListAPIView,
    OrderDetailAPIView,
    OrderCreateAPIView,

    WishlistItemCreateAPIView,
    WishlistItemDeleteAPIView,
)

app_name = 'Companyapi'

urlpatterns = [

    # company views
    path('', CompanyListAPIView.as_view(), name='list'),
    path('<int:pk>/', CompanyDetailAPIView.as_view(), name='detail'),
    path('create/', CompanyCreateAPIView.as_view(), name='create'),
    path('<pk>/update/', CompanyUpdateAPIView.as_view(), name='update'),
    path('<pk>/changepassword/',
         CompanyChangePasswordAPIView.as_view(), name='changepassword'),
    path('<pk>/delete/', CompanyDeleteAPIView.as_view(), name='delete'),

    # category views
    path('category/', CategoryListAPIView.as_view(), name='subcategorieslist'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(),
         name='categoriesdetail'),
    path('category/create/', CategoryCreateAPIView.as_view(),
         name='categoriescreate'),
    path('category/<pk>/update/', CategoryUpdateAPIView.as_view(),
         name='categoriesupdate'),
    path('category/<pk>/delete/', CategoryDeleteAPIView.as_view(),
         name='categoriesdelete'),

    # subcategory views
    path('subcategory/', SubcategoryListAPIView.as_view(),
         name='subcategorieslist'),
    path('subcategory/<int:pk>/', SubcategoryDetailAPIView.as_view(),
         name='subcategoriesdetail'),
    path('subcategory/create/', SubcategoryCreateAPIView.as_view(),
         name='subcategoriescreate'),
    path('subcategory/<pk>/update/', SubcategoryUpdateAPIView.as_view(),
         name='subcategoriesupdate'),
    path('subcategory/<pk>/delete/', SubcategoryDeleteAPIView.as_view(),
         name='subcategoriesdelete'),

    # product views
    path('product/', ProductListAPIView.as_view(),
         name='productlist'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(),
         name='productdetail'),
    path('product/create/', ProductCreateAPIView.as_view(),
         name='productcreate'),
    path('product/<pk>/update/', ProductUpdateAPIView.as_view(),
         name='productupdate'),
    path('product/<pk>/delete/', ProductDeleteAPIView.as_view(),
         name='productdelete'),


    # cart views
    path('cartitem/', CartItemListAPIView.as_view(),
         name='cartitemlist'),
    path('cartitem/<int:pk>/', CartItemDetailAPIView.as_view(),
         name='cartitemdetail'),
    path('cartitem/create', CartItemCreateAPIView.as_view(),
         name='cartitemcreate'),
    path('cartitem/<pk>/update/', CartItemUpdateAPIView.as_view(),
         name='cartitemupdate'),
    path('cartitem/<pk>/delete/', CartItemDeleteAPIView.as_view(),
         name='cartitemdelete'),

    # order views
    path('order/', OrderListAPIView.as_view(),
         name='orderlist'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(),
         name='orderdetail'),
    path('order/create', OrderCreateAPIView.as_view(),
         name='ordercreate'),


    # wishlist views
    path('addtowishlist/', WishlistItemCreateAPIView.as_view(),
         name='wishlistcreate'),
    path('deletefromwishlist/<int:pk>', WishlistItemDeleteAPIView.as_view(),
         name='wishlistdelete'),
]
