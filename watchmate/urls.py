"""watchmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
import rest_framework

import watch_list

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('movies/',include('watch_list.urls')), for api without framework
    path('watch/',include('watch_list.api.urls')),
    # using temporary login and logout of the drf for test purposes
    # remove becos we are implemeting our own authentication now
    
    # path('api-auth',include('rest_framework.urls'))
    
    # urls for user app and token authentication
    path('account/',include('user_app.api.urls')),
]
