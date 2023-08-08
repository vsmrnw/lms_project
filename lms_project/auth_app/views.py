from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User


def user_login(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Ваш аккаунт заблокирован')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        data = request.POST
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
                    birthday=data['birthday'], description=data['description'], avatar=data['avatar'])
        user.set_password(data['password'])
        user.save()
        pupil = Group.objects.filter(name='Ученик')
        user.groups.set(pupil)
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'register.html')


def change_password(request):
    return HttpResponse('Обработчик для смены пароля пользователя')


def reset_password(request):
    return HttpResponse('В обработчике реализована логика сброса пароля пользователя')
