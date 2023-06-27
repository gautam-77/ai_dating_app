from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers

from  .serializers import *
import requests
from rest_framework import status


# Create your views here.
class RegisterUser(APIView):
    
    def get(self):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            user_email = request.data["email"].lower()
            user_already_exists = User.objects.filter(email=user_email).exists()
            
            if user_already_exists:
                return Response({"message": "User already exists with the given email address.", "data": None}, status=status.HTTP_400_BAD_REQUEST)

            user = UserSerializer(data=request.data)
            if user.is_valid():
                user.save()
                return Response({"message": "success", "data": user.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": user.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
            user = UserSerializer(user, data=request.data, partial=True)
            
            if user.is_valid():
                user.save()
                return Response({"message": "success", "data": user.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": user.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({"message": "success", "data": None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)