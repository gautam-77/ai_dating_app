from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from django.contrib.auth.hashers import check_password
from .thread import Thradpooltest
# import django.contrib.auth.password_validation as validators

from  .serializers import *
import requests
from rest_framework import status



class UserGet(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
      
class UserAdd(APIView):
    def post(self, request):
        try:
            user_email = request.data["email"].lower()
            user_already_exists = User.objects.filter(email=user_email).exists()
            
            if user_already_exists:
                return Response({"message": "User already exists with the given email address.", "data": None}, status=status.HTTP_400_BAD_REQUEST)

            user = UserSerializer(data=request.data)
            if user.is_valid():
                user.save()
                session = request.session['email'] = user_email
                return Response({"message": "success", "data": user.data, 'session':session}, status=status.HTTP_200_OK)
            else:
                return Response({"message": user.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)  
     
class UserUpdate(APIView):
    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
            user = UserUpdateSerializer(user, data=request.data, partial=True)
            
            if user.is_valid():
                user.save()
                return Response({"message": "success", "data": user.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": user.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)
        
class UserDelete(APIView):
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({"message": "success", "data": None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)     
        
class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email = email)
        
        try:
            if user is not None:
                # print("thss-=-=-==-")
                # return Response({"message": "user is not exists", "data": None}, status=status.HTTP_400_BAD_REQUEST)
                if user.email == email and  check_password(password, user.password):
                    print("ths si s-=-=-==-")
                    session = request.session['email'] = user.email
                    Thradpooltest(email).start()
                    return Response({"message": "user is login", "data": None, 'session':session}, status=status.HTTP_200_OK)
                return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)   
                    
                    
class Resetpassword(APIView):
    def patch(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)
        serializer = UserPasswordResetSerializer(user, data=request.data,partial=True)
        if serializer.is_valid(): 
            serializer.save()
            return Response({"message": "password change", "data": None}, status=status.HTTP_200_OK)
        return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
