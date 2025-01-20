from django.urls import path
from .views import digest_authenticate

app_name = 'secret'

urlpatterns = [
    path('', digest_authenticate),
]