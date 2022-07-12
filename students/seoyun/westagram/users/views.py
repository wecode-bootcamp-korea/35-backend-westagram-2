import re
import json
import bcrypt

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from users.models     import User
from my_settings      import SECRET_KEY
class SignUpView(View):
    def post(self, request):
        try:
            user_data        = json.loads(request.body)
            name             = user_data['name']
            email            = user_data['email']
            password         = user_data['password']
            phone_number     = user_data['phone_number']

            email_check      = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            password_check   = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            if User.objects.filter(email=email):
                return JsonResponse({'message':'이미 가입된 이메일 입니다.'}, status=400)
            
            if not re.match(email_check,email):
                return JsonResponse({'message':'이메일 조건을 확인해주세요.'}, status=400)
            
            if not re.match(password_check, password):
                return JsonResponse({'message':'비밀번호 조건을 확인해주세요.'}, status=400)

            hashed_password  = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
                ).decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password,
                phone_number = phone_number
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            user_data  = json.loads(request.body)
            email      = user_data['email']
            password   = user_data['password']
            login_user = User.objects.get(email=email)
            
            if not (password == login_user.password):
                return JsonResponse({"message": "INVALID_USER_PASSWORD"}, status=401)
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER_EMAIL"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

