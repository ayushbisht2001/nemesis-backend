from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .jwtAuth import JWTAuthentication
# Create your views here.


class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):        
        response = dict()
        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():              
            serializer.save() 
            user = get_object_or_404(CustomUser, username=serializer.validated_data["username"])               
            response["data"] = serializer.data
            response["data"]["token"] = user.jwtToken.get("token", "")
            response["data"]["expires_at"] = user.jwtToken.get("expires_at", "")
            response["status"] = status.HTTP_201_CREATED
            response["msg"] = "Congo. You're successfully registered"
            return Response(response)
        else:
            return Response({"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST })


class LoginView(APIView):
    
    def post(self, request, *args, **kwargs):        
        email = request.data['email']
        password = request.data['password']

        user = get_object_or_404(CustomUser, email=email)  

        if not user  :
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')        
       
        response = {}
        response["data"]= {
            'username' : user.username,
            'token' : user.jwtToken.get("token",""),
            'expires_at' : user.jwtToken.get("expires_at", timezone.now)  
        }                     
        
        response["status"] = status.HTTP_200_OK
        response["msg"] = "You are Successfully logged in"           
        return Response(response)
      

class LogoutUserView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": status.HTTP_200_OK })


class UserMangerView(APIView):
    serializer_class  = UserProfileSerializers
    authentication_classes = (JWTAuthentication, )

    def delete(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=kwargs.get("id"))
        except CustomUser.DoesNotExist:
            return Response({"data" : 'User not found', "status" : status.HTTP_400_BAD_REQUEST})    
        user.delete()
        return Response({"data" : "User successfully deleted"})

    def patch(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=kwargs.get("id"))
        except CustomUser.DoesNotExist:
            return Response({"data" : 'User not found', "status" : status.HTTP_400_BAD_REQUEST})

        serializer = UserProfileSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(["GET"])
def get_user_list(request):
    users = CustomUser.objects.all()
    if users.exists():
        serializer = UserProfileSerializers(users, many=True) 
        return Response({'data' : serializer.data,'msg' : "User found",   'status' :status.HTTP_200_OK })
    
    else:
        return Response({'data': [],'msg' : "Users not found",  'status': status.HTTP_404_NOT_FOUND})


