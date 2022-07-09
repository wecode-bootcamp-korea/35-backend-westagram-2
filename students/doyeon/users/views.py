import json
import re

from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from users.models import User

class UserView(View):
    def post(self, request):
        """
        목적 : 클라이언트로 부터 들어오는 회원가입 정보를 데이터베이스에 저장

        1. 클라이언트로 부터 들어오는 정보
        - 이름
        - email
        - 패스워드
        - 핸드폰번호

        2. 클라이언트로 들어오는 정보가 형식에 맞는지 판단
        - email이 형식에 맞는지 확인
        - 패스워드가 형식에 맞는지 확인
        - 휴대번호가 유닉크한 값인지 확인

        3. 출력
        - 형식에 맞다면 데이터베이스에 저장
        - 형식에 맞지 않다면 오류 발생
        """
        try:
            data         = json.loads(request.body)

            name         = data["name"]
            email        = data["email"]
            password     = data["password"]
            phone_number = data["phone_number"]

            regx_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regx_password = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'


            if len(email) or len(password) == 0:
                raise KeyError
            if re.compile(regx_email).match(email) is None:
                raise KeyError
            if re.compile(regx_password).match(password) is None:
                raise KeyError
            if User.objects.filter(email=email).exist():
                raise KeyError

            user = User.object.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
                create_at    = timezone.now(),
                update_at    = timezone.now(),
            )
            return JsonResponse({"message":"Success"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KeyError"}, status=400)