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
                return JsonResponse({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
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
        if (not params.get("name")) or (len(params.get("name")) > 8): # not a valid name
            return JsonResponse({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        if (params.get("amount") != None) and (not isinstance(params.get("amount"), int) or params.get("amount") < 0): # not a valid amount
            return JsonResponse({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        if Inventory.objects.filter(product=params.get("name")).exists():
            item = Inventory.objects.get(product=params.get("name"))
            item.quantity += params.get("amount") or 1
            item.save()
        else:
            Inventory.objects.create(
                product = params.get("name"),
                quantity = params.get("amount") or 1
            )                
        location = f"http://35.78.106.61:80/v1/stocks/{params.get('name')}"
        response = JsonResponse(params, status=status.HTTP_200_OK)
        response['Location'] = location
        return response
    
    def delete(self, request):
        Inventory.objects.all().delete()
        return Response(status = status.HTTP_200_OK)

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
        if (params.get("amount") != None) and (not isinstance(params.get("amount"), int) or params.get("amount") < 0): # not a valid amount
            return JsonResponse({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        if (params.get("price") != None): # not a valid price
            if not (isinstance(params.get("price"), int) or isinstance(params.get("price"), float)) or params.get("price") < 0:
                return JsonResponse({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        item = Inventory.objects.filter(product=params.get("name")).first()
        if item == None or item.quantity < (params.get("amount") or 1):
            return JsonResponse({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            item.quantity -= (params.get("amount") or 1)
            exist = Inventory.objects.filter(product="sales").exists()
            if not exist: 
                Inventory.objects.create(product="sales", quantity=0)
            profit = Inventory.objects.get(product="sales")
            profit.quantity += int((params.get("amount") or 1) * (params.get("price") or 0) * 10000)
            item.save()
            profit.save()
            location = f"http://35.78.106.61:80/v1/sales/{params.get('name')}"
            response = JsonResponse(params, status = status.HTTP_200_OK)
            response['Location'] = location
            return response