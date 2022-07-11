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

            check_regx(regx_email, email, "EMAIL")
            does_existed(email, "EMAIL")
            check_regx(regx_password, password, "PASSWORD")
            check_regx(regx_phone_number, phone_number, "PHONE_NUMBER")
            does_existed(phone_number, "PHONE_NUMBER")

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

def check_regx(pattern, field_data, target_field):
    if not re.compile(pattern).match(field_data):
        raise ValueError(f"INVILD_{target_field}")

def does_existed(data, target_field):
    if User.objects.is_existed(data).exists():
        raise ValueError(f"EXISTED_{target_field}")