# import hashlib
# from django.http import HttpResponse
# from rest_framework.response import Response
# from rest_framework import status

# USERNAME = "aws"
# PASSWORD = "candidate"

# def digest_authenticate(request):
#     auth_header = request.META.get("HTTP_AUTHORIZATION")

#     if auth_header and auth_header.startswith("Digest "):
#         auth_data = {}
#         for part in auth_header[7:].split(", "):
#             key, value = part.split("=")
#             auth_data[key] = value.strip('"')

#         ha1 = hashlib.md5(f"{USERNAME}:{auth_data['realm']}:{PASSWORD}".encode()).hexdigest()
#         ha2 = hashlib.md5(f"{request.method}:{auth_data['uri']}".encode()).hexdigest()
#         expected_response = hashlib.md5(f"{ha1}:{auth_data['nonce']}:{ha2}".encode()).hexdigest()

#         if auth_data.get("response") == expected_response:
#             return HttpResponse("SUCCESS", status=status.HTTP_200_OK)
#     return HttpResponse("FAIL", status=status.HTTP_401_UNAUTHORIZED)

import base64
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

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

