from rest_framework import serializers 
from .models import *
from django.shortcuts import get_object_or_404
from .models import CustomUser




class RegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ("username","email",  "password", "password2", "address")
        extra_kwargs = {
        'password' : {'write_only': True},
        'address' : {'write_only': True},
        'email' : {'write_only' : True}
        }

    def save(self):
        user = CustomUser(
            username = self.validated_data["username"], email = self.validated_data["email"]
        )
        password = self.validated_data['password']
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({'password': 'Password Fields are not same.'})

        if CustomUser.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({'username': 'User with this name already Exists'})
        
        if CustomUser.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"email" : "Email address already taken"})

        user.set_password(password)
        user.address = self.validated_data["address"]
        user.save()
        return user



class UserProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ( 'username', 'email', 'address')
        extra_kwargs = {
            'username' : {'required' : False}
        }
