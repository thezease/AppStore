"""AppStore URL Configuration

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
    path('admin_dashboard', app.admin.dashboard, name = 'admin_dashboard'),
    path('admin_users', app.admin.users, name = 'admin_users'),
    path('admin_users_edit/<str:id>', app.admin.users_edit, name = 'admin_users_edit'),
    path('admin_users_view/<str:id>', app.admin.users_view, name = 'admin_users_view'),
    path('admin_users_add', app.admin.users_add, name = 'admin_users_view'),
    path('admin_statistics', app.admin.statistics, name = 'admin_statistics'),
    path('admin_apartments', app.admin.apartments, name = 'admin_aparments'),
    path('admin_apartments_edit/<str:id>', app.admin.apartments_edit, name = 'admin_apartments_edit'),
    path('rating_rank', app.admin.rating_rank, name = 'rating_rank'),
    path('', app.views.index, name='index'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('checkpw/<str:id>', app.views.checkpw, name='checkpw'),
    path('search', app.views.search, name='search'),
    path('apartment/<str:id>', app.views.apartment, name='apartment'),
    path('users', app.views.users, name='users')
]
