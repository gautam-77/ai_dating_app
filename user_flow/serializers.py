from .models import *

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
# import django.contrib.auth.password_validation as validators
from .dictdata import textreplay


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate_password(self, password):
        return make_password(password)
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']
   
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def validate_password(self, password):
        return make_password(password)

class UserPasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
    
    def validate_password(self, password):
        return make_password(password)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = '__all__'    

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = ['city','image','link']

class ImageTextSearlizer(serializers.ModelSerializer):
    class Meta:
        model = Imagetotext
        fields = ['image_file', 'user', 'image_text']
        
        # def to_representation(self, instance):
        #     data = super().to_representation(instance)
        #     x  = textreplay()
        #     print(x,'-=-')
        #     data['image_text'] = x
        #     return data