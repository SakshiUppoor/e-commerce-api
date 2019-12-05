
from django.urls import path
from django.conf.urls import include
from customer import views

app_name = 'customer'

urlpatterns = [
    path('register/', views.register, name="signup"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="logout"),
    path('customer/api/', include("customer.api.urls")),
]
