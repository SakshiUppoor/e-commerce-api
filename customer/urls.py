
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from customer import views

app_name = 'customer'

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('register/', views.register, name="signup"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="logout"),
    path('customer/api/', include("customer.api.urls")),
]
