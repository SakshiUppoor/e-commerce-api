from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet

app_name = 'customerapi'

router = DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = router.urls
