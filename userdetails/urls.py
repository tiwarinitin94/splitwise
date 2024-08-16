from django.urls import path
from . import views

from django.contrib.auth import views as auth_views




urlpatterns = [
   path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='userlogin'),
    path('user_list/', views.UserListAPIView.as_view(), name='userlist'),
    
]
