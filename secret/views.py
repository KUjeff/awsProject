import hashlib
from django.http import HttpResponse
from rest_framework import status

USERNAME = "aws"
PASSWORD = "candidate"

def digest_authenticate(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")

    if auth_header and auth_header.startswith("Digest "):
        auth_data = {}
        for part in auth_header[7:].split(", "):
            key, value = part.split("=")
            auth_data[key] = value.strip('"')

        ha1 = hashlib.md5(f"{USERNAME}:{auth_data['realm']}:{PASSWORD}".encode()).hexdigest()
        ha2 = hashlib.md5(f"{request.method}:{auth_data['uri']}".encode()).hexdigest()
        expected_response = hashlib.md5(f"{ha1}:{auth_data['nonce']}:{ha2}".encode()).hexdigest()

        if auth_data.get("response") == expected_response:
            return HttpResponse("SUCCESS")
    return HttpResponse("FAIL", status=status.HTTP_401_UNAUTHORIZED)
