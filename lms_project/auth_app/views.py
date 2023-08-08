from django.contrib.auth import authenticate, login, logout
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
        new_user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
                    birthday=data['birthday'], description=data['description'], avatar=data['avatar'])
        new_user.set_password(data['password'])
        new_user.save()
        pupil = Group.objects.filter(name='Ученик')
        new_user.groups.set(pupil)
        login(request, new_user)
        return redirect('index')
    else:
        return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return redirect('user_login')


def change_password(request):
    return HttpResponse('Обработчик для смены пароля пользователя')


def reset_password(request):
    return HttpResponse('В обработчике реализована логика сброса пароля пользователя')
