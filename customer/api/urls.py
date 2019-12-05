from django.urls import path

from .views import (
    CustomerListAPIView,
    CustomerDetailAPIView,
    CustomerCreateAPIView,
    CustomerUpdateAPIView,
    CustomerDeleteAPIView,
    CustomerChangePasswordAPIView,
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
]
