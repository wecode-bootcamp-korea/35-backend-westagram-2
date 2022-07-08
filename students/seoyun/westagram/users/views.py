import json
import re

from django.http      import JsonResponse
from django.shortcuts import render
from django.views     import View

from users.models     import User

class SignUpView(View):
    def post(self,request):
        try:
            user_data      = json.loads(request.body)
            name           = user_data['name']
            password       = user_data['password']
            phone_number   = user_data['phone_number']
            email          = user_data['email']
            
            email_check    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_check = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(password_check, password):
                return JsonResponse({"message": "비밀번호 조건에 부합하지 않습니다."}, status=400)

            if not re.match(email_check, email):
                return JsonResponse( {"message": "이메일 조건에 부합하지 않습니다."}, status=400)
            
            if User.objects.filter(email=email):
                return JsonResponse({"message": "이미 가입된 이메일 입니다."}, status=400)

            User.objects.create(
                name         = name,
                password     = password,
                email        = email,
                phone_number = phone_number
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse( {"message": "KEY_ERROR"}, status=400)


