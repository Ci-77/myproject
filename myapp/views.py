
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from myapp.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def hello(request):
    # HttpResponse是一个Http响应对象
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    request.method
    # render渲染模版
    return render(request, 'index.html')

# 原来是这样子的 
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
               return JsonResponse({'code':-1,'msg':'用户名或密码不能为空'})
           userInfo = User.objects.filter(username=username).first()
           if userInfo is None:
               return JsonResponse({'code':-1,'msg':'用户不存在'})
           if userInfo.password!=password:
               return JsonResponse({'code':-1,'msg':'密码错误'})
           
           return JsonResponse({'code':0,'msg':'登录成功'})
               
       except:
           return JsonResponse({'code':-1,'msg':'请求格式错误'})

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
            user = User(username=username,password=password)
            user.save()
            return JsonResponse({'code':0,'msg':'注册成功'})
        except:
            return JsonResponse({'code':-1,'msg':'请求格式错误'})

            

    return HttpResponse('注册成功')