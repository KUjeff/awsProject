from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Inventory
from django.http import JsonResponse

class StockView(APIView):  
    def get(self, request, name=None):
        if name:
            item = Inventory.objects.filter(product=name).first()
            if not item:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            response = {item.product: item.quantity}
            return JsonResponse(
                response,
                status=status.HTTP_200_OK
            )
        items = Inventory.objects.all().values("product", "quantity")
        response = {item["product"]: item["quantity"] for item in items if item["product"] != "sales"}
        return JsonResponse(
            response,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        params = request.data
        exist = Inventory.objects.filter(product=params.get("name")).exists()
        if exist:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            Inventory.objects.create(
                product = params.get("name"),
                quantity = params.get("amount") or 1
            )                
            location = f"http://180.144.199.108:80/v1/stocks/{params.get('name')}"
            response = JsonResponse(params)
            response['Location'] = location
            return response
    
    def delete(self, request):
        Inventory.objects.all().delete()
        return JsonResponse(status = status.HTTP_200_OK)

class SaleView(APIView):
    def get(self, request):
        exist = Inventory.objects.filter(product="sales").exists()
        if exist:
            profit = float(Inventory.objects.get(product="sales").quantity)/10000
            return JsonResponse(
                {"sales": round(profit, 2)},
                status=status.HTTP_200_OK
            )
        else:
            Inventory.objects.create(product="sales", quantity=0)
            return JsonResponse(
                {"sales": 0.0},
                status = status.HTTP_200_OK
            )
    
    def post(self, request):
        params = request.data
        item = Inventory.objects.filter(product=params.get("name")).first()
        if item == None or item.quantity < (params.get("amount") or 1):
            return JsonResponse(status = status.HTTP_400_BAD_REQUEST)
        else:
            item.quantity -= (params.get("amount") or 1)
            exist = Inventory.objects.filter(product="sales").exists()
            if not exist: 
                Inventory.objects.create(product="sales", quantity=0)
            profit = Inventory.objects.get(product="sales")
            profit.quantity += int((params.get("amount") or 1) * (params.get("price") or 0) * 10000)
            item.save()
            profit.save()
            location = f"http://180.144.199.108:80/v1/sales/{params.get('name')}"
            response = JsonResponse(params, status = status.HTTP_200_OK)
            response['Location'] = location
            return response