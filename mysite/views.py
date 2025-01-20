from django.http import HttpResponse
import hashlib

def home(request):
    return HttpResponse("AWS")