"""
URL configuration for Detection_and_Analysis_of_Pill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views as mv
from Admin import views as av
from user import views as uv

urlpatterns = [
    path('admin/', admin.site.urls),

    #mainView urls
    path('',mv.index,name='index'),
    path('adminLoginForm',mv.adminLoginForm,name='adminLoginForm'),
    path('userLoginForm',mv.userLoginForm,name='userLoginForm'),
    path('userRegisterForm',mv.userRegisterForm,name='userRegisterForm'),

    #adminUrls
    path('adminLoginCheck',av.adminLoginCheck,name='adminLoginCheck'),
    path('adminHome',av.adminHome,name='adminHome'),
    path('userDetails',av.userDetails,name='userDetails'),
    path('activateUser',av.activateUser,name='activateUser'),
    path('deactivateUser',av.deactivateUser,name='deactivateUser'),
    path('adminclassificationView',av.adminclassificationView,name='adminclassificationView'),

    #userurls
    path('userHome',uv.userHome,name='userHome'),
    path('userRegister',uv.userRegister,name='userRegister'),
    path('userLoginCheck',uv.userLoginCheck,name='userLoginCheck'),
    path('dataset',uv.dataset,name='dataset'),
    path('predict_heart_disease',uv.predict_heart_disease,name='predict_heart_disease'),
    path('classificationView',uv.classificationView,name='classificationView'),


    
    

    
    
]
