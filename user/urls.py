from django.contrib import admin 
from django.urls import path, include
from .views import *

urlpatterns = [

    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/',LogoutUserView.as_view(), name="logout" ),     
    path('delete_user/<str:id>/',  UserMangerView.as_view(), name="delete_user"),
    path('update_user/<str:id>/',  UserMangerView.as_view(), name="update_user"),
    path('get_users_list/', get_user_list, name="user_list"), 

]