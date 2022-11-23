import json
import uuid
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
import uuid
# Create your views here.
from rest_framework.views import APIView
from api import models
# def login(request):
#     return render(request, 'login.html')
class LoginView(APIView):
    # 用户登录
    def post(self,request,*args,**kwargs):
        user=request.data.get('username')
        pwd = request.data.get('password')

        user_object =models.UserInfo.objects.filter(username=user,password=pwd)
        if not user_object:
            msg={'code':1000,'error':"用户名或密码错误"}
            return Response({'code': 1000, 'error': "用户名或密码错误"})
            #return render(request,"logined.html",{'msg':json.dumps(msg)})
        random_string =str(uuid.uuid4())
        #random_string="666"
        for i in range(len(user_object)):
            user_object[i].token = random_string
            user_object[i].save()
            msg={'code':1001,'data':random_string}
        return Response (msg)
       # return render(request,"logined.html",{'msg':json.dumps(msg)})

class OrderView(APIView):
    def get(self,request,*args,**kwargs):
        token =request.query_params.get("token")
        if not token:
            return Response({'code':2000,'error':"登录成功之后才能访问"})
        user_object = models.UserInfo.objects.filter(token=token).first()
        if not user_object:
            return Response({'code':2000,'error':"token无效"})

        return Response('订单列表')

class JwtLoginView(APIView):
    # 用户登录
    def post(self,request,*args,**kwargs):
        user=request.data.get('username')
        pwd = request.data.get('password')

        user_object =models.UserInfo.objects.filter(username=user,password=pwd)
        if not user_object:
            msg={'code':1000,'error':"用户名或密码错误"}
            return Response({'code': 1000, 'error': "用户名或密码错误"})
            #return render(request,"logined.html",{'msg':json.dumps(msg)})

        import jwt
        import datetime
        SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='
        # 构造header
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        payload = {
            'user_id': 1,  # 自定义用户ID
            'username': "xj",  # 自定义用户名
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # 超时时间
        }
        result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
        #random_string =str(uuid.uuid4())
        random_string=result


        for i in range(len(user_object)):
            user_object[i].token = random_string
            user_object[i].save()
            msg={'code':1001,'data':random_string}
        return Response (msg)
       # return render(request,"logined.html",{'msg':json.dumps(msg)})


class JwtOrderView(APIView):
    def get(self,request,*args,**kwargs):
        token =request.query_params.get("token")
        import jwt
        from jwt import exceptions
        SALT= 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='
        verified_payload = None
        msg=None
        try:
            # 从token中获取payload【不校验合法性】
            # unverified_payload = jwt.decode(token, None, False)
            # print(unverified_payload)
            # 从token中获取payload【校验合法性】
            verified_payload = jwt.decode(token, SALT, algorithms=["HS256"])
            #return verified_payload
        except exceptions.ExpiredSignatureError:
            msg='token已失效'
        except jwt.DecodeError:
            msg='token认证失败'
        except jwt.InvalidTokenError:
            msg='非法的token'

        if not verified_payload:
            return Response({'code':1003, 'error':msg})

        return Response({'code':1004,'msg':"验证通过"})
        # if not token:
        #     return Response({'code':2000,'error':"登录成功之后才能访问"})
        # user_object = models.UserInfo.objects.filter(token=token).first()
        # if not user_object:
        #     return Response({'code':2000,'error':"token无效"})
        #
        # return Response('订单列表')

# from api.extensions.auth import JwtQueryParamsAuthentication
# class ProOrderView(APIView):
#     authentication_classes = [JwtQueryParamsAuthentication,]
#     def get(self,request,*args,**kwargs):
#         pass