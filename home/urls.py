from django.contrib import admin
from django.urls import path,include

from .import views

urlpatterns = [
    
    path('home', views.home,name ="home"),
    path('',views.login,name='login'),
    path('logouthome',views.logouthome,name='logouthome'),
    path('signup',views.signup,name='signup'),
    path('admindash',views.admindash,name='admindash'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('cuser',views.cuser,name='cuser'),
    path('alogout',views.alogout,name='alogout'),
    path('admin_delete<str:pk>',views.admin_delete,name='admin_delete'),
    path('admin_edit<str:user_id>',views.admin_edit,name='admin_edit'),
    
    
]