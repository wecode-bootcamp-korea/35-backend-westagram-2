import json

from django.http import JsonResponse
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
        data = json.loads(request.body)
        if user_name = None or user_eamil



    return JsonResponse({'message':'created'}, status=201)