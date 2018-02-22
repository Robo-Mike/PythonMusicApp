from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#this routes the rurl to the inbuilt views r = regex, framework expects template under templates/registration folder
urlpatterns = [path('',views.index,name='index'),path('login', auth_views.login, name='login')]
