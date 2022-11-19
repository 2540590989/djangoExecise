import uuid

from django.shortcuts import render
from rest_framework.response import Response
import uuid
# Create your views here.
from rest_framework.views import APIView
from api import models

class LoginView(APIView):
    # 用户登录
    def post(self,request,*args,**kwargs):
        user=request.data.get('username')
        pwd = request.data.get('password')

        user_object =models.UserInfo.objects.filter(username=user,password=pwd)
        if not user_object:
            return Response({'code':1000,'error':"用户名或密码错误"})

        random_string =str(uuid.uuid4())
        #random_string="666"


        for i in range(len(user_object)):
            user_object[i].token = random_string
            user_object[i].save()
        return Response ({'code':1001,'data':random_string})

class OrderView(APIView):
    def get(self,request,*args,**kwargs):
        token =request.query_params.get("token")
        if not token:
            return Response({'code':2000,'error':"登录成功之后才能访问"})
        user_object = models.UserInfo.objects.filter(token=token).first()
        if not user_object:
            return Response({'code':2000,'error':"token无效"})

        return Response('订单列表')