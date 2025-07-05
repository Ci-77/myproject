
import json
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from myapp.models import User
from django.views.decorators.csrf import csrf_exempt
from myapp.utils import response,token,pwd
import datetime as datetime
# Create your views here.

def login(request):
    if request.method=='POST':
       try:
           data =json.loads(request.body)
           username = data.get('username','')
           password = data.get('password','')
           if username==''or password=='':
               return response.ResponseError("username or password is err")
           userInfo = User.objects.filter(username=username).first()
           if userInfo is None:
               return response.ResponseError('username not exists')
           if not pwd.check_password(password,userInfo.password):
               return response.ResponseError("password err")
           ## 颁发token
           myToken =token.generate_token(userInfo.id)
           return response.ResponseSuccess(myToken,"登录成功")
               
       except Exception as e:
         traceback.print_exc()

def register(request):
    if request.method=='POST':
        try:
            data =json.loads(request.body)
            username = data.get('username','')
            password = data.get('password','')
            confirmPassword = data.get('confirmPassword','')
            if username==''or password==''or confirmPassword=='':
                return response.ResponseError("username or password err")
            if password!=confirmPassword:
                return response.ResponseError("password err")
            if User.objects.filter(username=username).first():
                return response.ResponseError("user is exists")
            now_time =datetime.datetime.now()
            now =now_time.strftime('%Y-%m-%d %H:%M:%S')
            hashPassword = pwd.generate_password(password)

            user = User(username=username,password=hashPassword,created_at=now,updated_at=now)
            user.save()
            return response.ResponseSuccess("register successful")

        except Exception as e:
          traceback.print_exc()