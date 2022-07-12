import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            check_email    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            check_password = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            user_name         = data['name']
            user_email        = data['email']
            user_password     = data['password']
            user_phone_number = data['phone_number']

            if User.objects.filter(email=user_email).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
            if not re.match(check_email, user_email):
                return JsonResponse({'message': 'EMAIL_NOT_MATCH'}, status=400)
            if not re.match(check_password, user_password):
                return JsonResponse({'message': 'PASSWORD_NOT_MATCH'}, status=400)

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name         = user_name,
                email        = user_email,
                password     = decoded_password,
                phone_number = user_phone_number
            )
            return JsonResponse({'message': 'CREATED'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            email     = user_data['email']
            password  = user_data['password']

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'token': access_token}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
