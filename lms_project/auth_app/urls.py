from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', reset_password, name='reset_password'),
]
