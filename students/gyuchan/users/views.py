import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class UsersView(View):
    '''
    client에게 사용자 정보를 받음
    이메일이나 패스워드가 전달 되지 않으면(=입력하지 않으면) {"message": "KEY_ERROR"}, status code 400 반환
    이메일에는 @, .을 필수로 포함 없으면 에러
    비밀번호는 8자리 이상, 문자, 숫자, 특수문자의 복합 없으면 에러
    회원가입 시 이미 등록된 이메일이면 에러
    회원가입 성공하면 {"message":"SUCCESS"}, status code 201
    '''
    def post(self, request):
        '''
        request.body = {
            "name" : ,
            "email" : ,
            "password" : ,
            "phone_number" : 
        }
        '''
        try:
            data           = json.loads(request.body)
            check_email    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            check_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
            
            user_name         = data['name']
            user_email        = data['email']
            user_password     = data['password']
            user_phone_number = data['phone_number']
            
            if user_email == '' or user_password == '':  # 이메일 비밀번호 작성 오류
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            if User.objects.filter(email=user_email).exists():  # 이메일 중복 오류 성공
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=400)
            if check_email.match(user_email) == None:  # 이메일 오류 성공
                return JsonResponse({'message':'EMAIL_NOT_MATCH'}, status=400)
            if check_password.match(user_password) == None:  # 비밀번호 오류 성공
                return JsonResponse({'message':'PASSWORD_NOT_MATCH'}, status=400)

            
            User.objects.create(
                name         = user_name,
                email        = user_email,
                password     = user_password,
                phone_number = user_phone_number
            )
            return JsonResponse({'message':'CREATED'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def get(self, request):
        '''
        request.body = {
            "email" = '',
            "password" = ''
        }
        '''