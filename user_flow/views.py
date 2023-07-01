from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from django.contrib.auth.hashers import check_password
from .thread import Thradpooltest
from .imgtotext import imagetotext
from .dictdata import textreplay, generate_custom_token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token




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
            print(user,'-=-=ssas')
            if user.is_valid():
                user.save()
                x =user.data['name']
                print(user.data,'-=--=-')
                print(request.data,'=--=')
                print(request.user,'=-ddd-=')
               
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
        print(user,'-=-=')
        # token_obj = Token.objects.get_or_create(user=user)
        # print(token_obj,'-==-0000')
        # print(x,'-=-=-=-==--=')
        try:
            if user is not None:
                if user.email == email and  check_password(password, user.password):
                    print("ths si s-=-=-==-")
                    session = request.session['email'] = user.email
                    Thradpooltest(email).start()
                    x = generate_custom_token(user)
                    # token_obj = Token.objects.get_or_create(user=user)
                    return Response({"message": "user is login", "data": request.data, 'session':session,'Token':x}, status=status.HTTP_200_OK)
                return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)   
                          
                                            
class Resetpassword(APIView):
    def patch(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email = email)
        print(user,'-=-==-')
        try:
            if user:
                serializer = UserPasswordResetSerializer(user, data=request.data, partial=True)
                if serializer.is_valid(): 
                    serializer.save()
                    return Response({"message": "password change", "data": None}, status=status.HTTP_200_OK)
                return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("-=-=-=-=")
                return Response({"message": "invalid credentials", "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)

class ProfileSet(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def get(self, reuqets):
        try:
            profile = Profile.objects.all()
            serializer = UserProfileSerializer(profile, many=True)
             
         
            return Response({"message":"profile data", "data":serializer.data, })
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = UserProfileSerializer(data = request.data)
        id = request.data.get('user')
     
        try:
            if Profile.objects.filter(user = id).exists():
                return Response({"msg":"already user exists"})
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"profile create", "data":serializer.data})
            return Response({"message": "profile not created", "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdate(APIView):
    def patch(self, request, id):
        datas = Profile.objects.get(user = id)
        print(datas,'-=-=')
        # token_obj = Token.objects.get_or_create(user=datas)
        # print(str(token_obj.key),'-==--=')
        serializer = UserProfileUpdateSerializer(datas , data = request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"profile updated", "data":serializer.data})    
            return Response({"message": "profile not updated", "data": None}, status=status.HTTP_400_BAD_REQUEST)            
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)      
                    
class ProfileDelete(APIView):
    def delete(self, request, id):
        try: 
            if id:
                profile = Profile.objects.get(user = id)            
                profile.delete()
                return Response({"message": "profile delete", "data": None}, status=status.HTTP_200_OK)
            return Response({"message": "id is not found", "data": None}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({"message": f"{e}", "data": None}, status=status.HTTP_400_BAD_REQUEST)  
        
  
class ImageToText(APIView):  
    def post(self, request):
        xx = request.data.get('image_file')
        print(xx,'==-=-')
        serializer = ImageTextSearlizer(data=request.data)
        # x = test(op)
        if serializer.is_valid():
            serializer.save()
            print('-=-=-=-=-=-==--=')
            data =  serializer.data['image_file']
            print(data,'===')
            x = imagetotext(data)
            data = x.replace('\n','')
            y = textreplay(data)
            print(y,'==-=')
            # print(d,'-=-=-=--0')
            return Response({'msg':serializer.data})
        return Response({'msg':"not working"})
        