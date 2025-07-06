
import json
from myapp.utils import response,redis
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from myapp.utils import token

# 验证登录token
class TokenAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                request.data = data
            except Exception:
                request.data = {}
        if request.path in ['/api/login', '/api/register']:
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response.ResponseError("Token is missing")

        user_id = token.validate_token(auth_header)
        if not user_id:
            return response.ResponseError("Token is invalid")
        userId =cache.get(user_id)
        if not userId:
            return response.ResponseError("Token is invalid")
        request.userId = userId
       # 自动续期token
        cache.expire(user_id,redis.TOKEN_EXPIRE)
        return self.get_response(request)
    

           

