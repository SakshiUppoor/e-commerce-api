from django.urls import path

from .views import (
    CustomerListAPIView,
    CustomerDetailAPIView,
    CustomerCreateAPIView,
    CustomerUpdateAPIView,
    CustomerDeleteAPIView,
    CustomerChangePasswordAPIView,
    CartItemListAPIView,
    CartItemDetailAPIView,
)

app_name = 'customerapi'

urlpatterns = [
    path('', CustomerListAPIView.as_view(), name='list'),
    path('list/<pk>/', CustomerDetailAPIView.as_view(), name='detail'),
    path('create/', CustomerCreateAPIView.as_view(), name='create'),
    path('<pk>/update/', CustomerUpdateAPIView.as_view(), name='update'),
    path('<pk>/changepassword/',
         CustomerChangePasswordAPIView.as_view(), name='changepassword'),
    path('<pk>/delete/', CustomerDeleteAPIView.as_view(), name='delete'),
    path('cart/', CartItemListAPIView.as_view(),
         name='cartitemlist'),
    path('cart/<int:pk>/', CartItemDetailAPIView.as_view(),
         name='cartitemdetail'),
]
