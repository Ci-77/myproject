
import json
import traceback
from myapp.models import User
from django.views.decorators.csrf import csrf_exempt
from myapp.utils import response,token,pwd,redis
import datetime as datetime
from django.core.cache import cache
# Create your views here.

def login(request):
    if request.method=='POST':
       try:
           print(request.data)
           data = request.data
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
           print(myToken)
           # 将token存到redis
           print(userInfo.id)
           cache.set(f"{userInfo.id}",myToken,redis.TOKEN_EXPIRE)
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

def logout(request):
    try:
    # 退出登录就是将token过期
        header = request.headers.get('Authorization')
        if not token:
            return response.ResponseError("token is null")
        user_id = token.validate_token(header)
        if not user_id:
            return response.ResponseError("token is invalid")
        cache.delete(f"{user_id}")
        return response.ResponseSuccess("logout successful")
    except Exception as e:
        traceback.print_exc()