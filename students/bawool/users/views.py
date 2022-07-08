import json

from time import clock_settime

from django.http import JsonResponse
from django.views import View

from .models import User

# Create your views here.

class SignupView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']
            phone    = data['phone']
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            User.objects.create(
                name     = name,
                email    = email,
                password = password,
                phone    = phone
                )
        

