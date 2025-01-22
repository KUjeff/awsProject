from django.urls import path
from .views import authenticate

app_name = 'secret'

urlpatterns = [
    path('', authenticate),
]