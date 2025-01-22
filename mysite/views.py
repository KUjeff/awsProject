from django.http import HttpResponse
import base64
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

# -------------------------------------------

def home(request):
    return HttpResponse("AWS")


# -------------------------------------------

USERNAME = "aws"
PASSWORD = "candidate"

def authenticate(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")

    if auth_header:
        encoded_credentials = auth_header[6:]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        
        username, password = decoded_credentials.split(":")

        if username == USERNAME and password == PASSWORD:
            return HttpResponse("SUCCESS", status=status.HTTP_200_OK)
    
    return HttpResponse("FAIL", status=status.HTTP_401_UNAUTHORIZED)