
# 封装一下JsonResponse
from django.http import JsonResponse

def ResponseSuccess(data,msg="success"):
    """
    返回一个成功的jsonResponse
    """
    response ={"code":0,"msg":msg,"data":data}
    return JsonResponse(response)

def ResponseError(msg):
    """
    返回一个错误响应
    """
    response = {"code":-1,"msg":msg,"data":None}
    return JsonResponse(response)