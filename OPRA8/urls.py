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
    
    path('admin_login', app.admin.login, name = 'admin_login'),
    path('admin_dashboard', app.admin.dashboard, name = 'admin_dashboard'),
    path('admin_dashboard_activeGuest_rank', app.admin.dashboard_activeGuest_rank, name = 'admin_dashboard_activeGuest_rank'),
    path('admin_dashboard_rating_rank', app.admin.dashboard_rating_rank, name = 'dashboard_rating_rank'),
    path('admin_dashboard_lengthOfStay_rank', app.admin.dashboard_lengthOfStay_rank, name = 'dashboard_lengthOfStay_rank'),
    path('admin_dashboard_bookingNum_rank', app.admin.dashboard_bookingNum_rank, name = 'dashboard_bookingNum_rank'),
    path('admin_users', app.admin.users, name = 'admin_users'),
    path('admin_users_edit/<str:id>', app.admin.users_edit, name = 'admin_users_edit'),
    path('admin_users_view/<str:id>', app.admin.users_view, name = 'admin_users_view'),
    path('admin_users_add', app.admin.users_add, name = 'admin_users_add'),
    path('admin_statistics', app.admin.statistics, name = 'admin_statistics'),
    path('admin_apartments', app.admin.apartments, name = 'admin_apartments'),
    path('admin_apartments_edit/<str:id>', app.admin.apartments_edit, name = 'admin_apartments_edit'),
    path('admin_apartments_add', app.admin.apartments_add, name = 'admin_apartments_add'),
    path('admin_apartments_view/<str:id>', app.admin.apartments_view, name = 'admin_apartments_view'),
    path('admin_rentals', app.admin.rentals, name = 'admin_rentals'),
    path('admin_rentals_edit/<str:id>', app.admin.rentals_edit, name = 'admin_rentals_edit'),
    path('admin_rentals_add', app.admin.rentals_add, name = 'admin_rentals_add'),
    path('admin_bookings', app.admin.bookings, name = 'admin_bookings'),
    path('admin_bookings_edit/<str:id>', app.admin.bookings_edit, name = 'admin_bookings_edit'),
    path('admin_bookings_add', app.admin.bookings_add, name = 'admin_bookings_add'),
    
]
