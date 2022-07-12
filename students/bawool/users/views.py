import json, re
import bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from .models import User
from westagram.settings import SECRET_KEY, ALGORITHM

# Create your views here.

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']
            phone    = data['phone']

            email_check = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_check = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            if not re.match(email_check, email): 
                return JsonResponse({'message' : 'invalid_email'}, status=400)
            
            if not re.match(password_check, password): 
                return JsonResponse({'message' : 'invalid_password'}, status=400)

            if User.objects.filter(email=email).exists(): 
                return JsonResponse({'message' : 'existent_email'}, status=400)

            if User.objects.filter(name=name).exists(): 
                return JsonResponse({'message' : 'existent_name'}, status=400)

            if User.objects.filter(phone=phone).exists(): 
                return JsonResponse({'message' : 'existent_phone'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password,
                phone    = phone,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email = email)

            if not User.objects.filter(email = email).exists(): 
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')): 
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=401)

            token = jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'ACCESS_TOKEN' : token }, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        

