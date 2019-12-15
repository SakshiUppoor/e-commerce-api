
from django.urls import path
from django.conf.urls import include
from company import views

app_name = 'company'

urlpatterns = [
    path('api/', include("company.api.urls")),
]
