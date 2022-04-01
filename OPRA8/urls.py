"""OPRA8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

import app.views


urlpatterns = [
    # django's admin page; not used for this app
    path('admin/', admin.site.urls),

    # default homepage
    path('', app.views.index, name='index'),

    # list of apartments
    path('search', app.views.search, name='search'),

    # details of a single apartment
    path('apartment/<int:apt_id>', app.views.apartment, name='apartment'), 
    
    # login page
    path('login', app.views.login, name='login'), 

    # new user registration
    path('register', app.views.register, name='register'), 
    
    # homepage after login
    path('u=<str:email>~', app.views.user_index, name='user_index'), 
    
    # list of apartments after login
    path('u=<str:email>~/search', app.views.user_search, name='user_search'), 

    # details of a single apartment after login
    path('u=<str:email>~/apartment/<int:apt_id>', app.views.user_view_apt, name='user_view_apt'), 
    
    # user's personal page to show user details and rental history
    path('u=<str:email>~/viewself', app.views.viewself, name='viewself'),
    
    # user's personal page to manage apartments where user is the host
    path('u=<str:email>~/viewself-host', app.views.viewself_host, name='viewself-host'),
    
    # password check before user can edit his personal details
    path('u=<str:email>~/checkpw', app.views.checkpw, name='checkpw')

]
