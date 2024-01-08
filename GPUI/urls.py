from django.urls import path
from .import views

urlpatterns =[
path('',views.index,name ='index'),
path('login_register',views.login_register,name='login_register'),
path('signout',views.signout,name='signout'),
path('save_form_data',views.save_form_data,name='save_form_data'),
path('success/',views.login_succes,name='success'),
path('login',views.login,name='login'),


]   
