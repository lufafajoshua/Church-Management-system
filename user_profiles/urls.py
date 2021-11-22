from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', LoginView), #user login view, inbuilt
    path('accounts/logout/', LogoutView), #handle user logout
    path('register/', views.register, name='register'),
    path('myprofile/', views.my_profile, name='my_user_profile'),
]