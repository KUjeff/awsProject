from django.urls import path
from .views import home
from django.urls import path, include

urlpatterns = [
    path('', home),  
    path('secret/', include('secret.urls')),
    path('v1/', include('inventory.urls')),
]
