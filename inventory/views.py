from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Inventory
from math import ceil

'''
constraints
(1) params: name(required), length <= 8,
            amount, postive int
(3) params: name(required), length <= 8,
            amount, postive int
            price, postive int/float
'''

class StockView(APIView):  
    def get(self, request, name=None):
        if name: # name is given
            item = Inventory.objects.filter(product=name).first()
            if not item: # product does not exist in table
                return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {item.product: item.quantity},
                status=status.HTTP_200_OK
            )
        else: # name not given, give all product info
            items = Inventory.objects.all()
            return Response(
                {item.product: item.quantity for item in items if item.product != "sales"},
                status=status.HTTP_200_OK
            )

    def post(self, request):
        params = request.data
        # check input params are valid
        name = params.get("name")
        amount = params.get("amount")
        if name == None or len(name) > 8: # not a valid name
            return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        if amount != None and (not isinstance(amount, int) or amount <= 0): # not a valid amount
            return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Inventory.objects.filter(product=name).exists(): # add amount to an existing name
            item = Inventory.objects.get(product=name)
            item.quantity += amount or 1
            item.save()
        else: # register new name & amount 
            Inventory.objects.create(
                product = name,
                quantity = amount or 1
            )                
        response = Response(params, status=status.HTTP_200_OK)
        response['Location'] = f"http://{request.headers.get('Host')}/v1/stocks/{name}"
        return response
    
    def delete(self, request):
        Inventory.objects.all().delete()
        return Response(status = status.HTTP_200_OK)

class SaleView(APIView):
    def get(self, request):
        exist = Inventory.objects.filter(product="sales").exists()
        if exist: # sales exists in table
            profit = ceil(Inventory.objects.get(product="sales").quantity*1.0/100)*1.0/100
            return Response(
                {"sales": round(profit, 2)},
                status=status.HTTP_200_OK
            )
        else: # sales does not exist, set its value to 0
            Inventory.objects.create(product="sales", quantity=0)
            return Response(
                {"sales": 0.0},
                status = status.HTTP_200_OK
            )
    
    def post(self, request):
        params = request.data
        # check input params are valid
        name = params.get("name")
        amount = params.get("amount")
        price = params.get("price")
        if name == None or len(name) > 8: # not a valid name
            return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        if amount != None and (not isinstance(amount, int) or amount < 0): # not a valid amount
            return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        if price != None: # not a valid price
            if not (isinstance(price, float) or isinstance(price, int)) or price <= 0:
                return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
            
        item = Inventory.objects.filter(product=name).first()
        if item == None or item.quantity < (amount or 1): # no product or insufficient product
            return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            item.quantity -= (amount or 1)
            if not Inventory.objects.filter(product="sales").exists(): # create sales if not exist
                Inventory.objects.create(product="sales", quantity=0)
            profit = Inventory.objects.get(product="sales")
            profit.quantity += int((amount or 1) * (price or 0) * 10000)
            item.save()
            profit.save()
            response = Response(params, status = status.HTTP_200_OK)
            response['Location'] = f"http://{request.headers.get('Host')}/v1/sales/{name}"
            return response