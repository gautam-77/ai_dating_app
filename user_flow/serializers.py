from .models import *

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
# import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate_password(self, password):
        return make_password(password)
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']
   
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def validate_password(self, password):
        return make_password(password)
                                