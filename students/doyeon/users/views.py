import json
import re

from django.http import JsonResponse
from django.views import View

from .models import User

class UserView(View):
    def post(self, request):
        try:
            data              = json.loads(request.body)

            name              = data["name"]
            email             = data["email"]
            password          = data["password"]
            phone_number      = data["phone_number"]

            regx_email        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regx_password     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            regx_phone_number = '^\d{3}-\d{3,4}-\d{4}$'

            check_email_regx(regx_email, email)

            if User.objects.filter(email = email).exists():
                raise ValueError("EXISTED_EMAIL")

            check_password_regx(regx_password, password)
            check_phone_regx(regx_phone_number, phone_number)

            if User.objects.filter(phone_number = phone_number).exists():
                raise ValueError("EXISTED_PHONE-NUMBER")

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ValueError as e:
            return JsonResponse({"message": f"{e}"}, status=400)

def check_email_regx(pattern, field_data):
    if not re.compile(pattern).match(field_data):
        raise ValueError("INVILD_EMAIL")

def check_password_regx(pattern, field_data):
    if not re.compile(pattern).match(field_data):
        raise ValueError("INVILD_PASSWORD")

def check_phone_regx(pattern, field_data):
    if not re.compile(pattern).match(field_data):
        raise ValueError("INVILD_PHONE-NUMBER")