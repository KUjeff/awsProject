from django.urls import path
from .views import StockView, SaleView
from django.urls import path

app_name = 'v1'

urlpatterns = [
    path('stocks', StockView.as_view()),
    path('stocks/<str:name>', StockView.as_view()),
    path('sales', SaleView.as_view())
]
