
import json
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from myapp.models import User
from django.views.decorators.csrf import csrf_exempt
from myapp.utils import response
import datetime as datetime
# Create your views here.

def hello(request):
    # HttpResponse是一个Http响应对象
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    request.method
    # render渲染模版
    return render(request, 'index.html')

# 原来是这样子的 
# redirect进行重定向
def something(request):
    print(request.GET)
    print(request.POST)
    return redirect('https://www.baidu.com')

@csrf_exempt
def login(request):
    if request.method=='POST':
       try:
           data =json.loads(request.body)
           username = data.get('username','')
           password = data.get('password','')
           if username==''or password=='':
               return response.ResponseError("用户名或密码不能为空")
           userInfo = User.objects.filter(username=username).first()
           if userInfo is None:
               return response.ResponseError('用户不存在')
           if userInfo.password!=password:
               return response.ResponseError("密码错误")
           
           return response.ResponseSuccess(None,"登录成功")
               
       except Exception as e:
         traceback.print_exc()

@csrf_exempt
def register(request):
    if request.method=='POST':
        try:
            data =json.loads(request.body)
            username = data.get('username','')
            password = data.get('password','')
            confirmPassword = data.get('confirmPassword','')
            if username==''or password==''or confirmPassword=='':
                return JsonResponse({'code':-1,'msg':'用户名或密码不能为空'})
            if password!=confirmPassword:
                return JsonResponse({'code':-1,'msg':'两次密码输入不一致'})
            if User.objects.filter(username=username).first():
                return JsonResponse({'code':-1,'msg':'用户已存在'})
            now =datetime.datetime.now()  
            user = User(username=username,password=password,created_at=now,updated_at=now)
            user.save()
            return JsonResponse({'code':0,'msg':'注册成功'})

        except Exception as e:
          traceback.print_exc()

            

    return HttpResponse('注册成功')