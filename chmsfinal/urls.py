"""Chms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('churchaccounts.urls', namespace='churchaccounts')),
    path('accounts/', include('django.contrib.auth.urls')),#app used to create user login and logout views
    path('user_profiles/', include('user_profiles.urls')),
    path('blog_app/', include('blog_app.urls')),
    path('', include('django_chatter.urls')),
    #path('paypal/', include('paypal.standard.ipn.urls')),

]
