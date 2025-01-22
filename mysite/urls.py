from django.urls import path
from .views import home, authenticate
from django.urls import path, include

urlpatterns = [
    path('', home),  
    path('secret', authenticate),
    path('v1/', include('inventory.urls')),
]
