import json
import re

from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from .models import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data["name"]
            email = data["email"]
            password = data["password"]
            phone_number = data["phone_number"]

            regx_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regx_password = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if check_regx(regx_email, email):
                if User.objects.filter(email=email).exists():
                    raise ValueError("EXISTED E_MAIL")
            if check_regx(regx_password, password):
                if User.objects.filter(phone_number=phone_number).exists():
                    raise ValueError("EXISTED PHONE_NUMBER")

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ValueError as e:
            return JsonResponse({"message": f"{e}"}, status=400)

        else:
            user = User.objects.create(
                name=name,
                email=email,
                password=password,
                phone_number=phone_number,
                create_at=timezone.now(),
                update_at=timezone.now(),
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)


def check_regx(pattern, data):
    if re.compile(pattern).match(data) is None:
        raise ValueError("INVALID_PASSWORD")
        return False
    else:
        return True

