from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return HttpResponse('Страница для входа пользователя на сайт')


def register(request):
    return HttpResponse('Страница для регистрации пользователя')


def logout(request):
    return HttpResponse('Выход и перенаправление на страницу входа')


def change_password(request):
    return HttpResponse('Обработчик для смены пароля пользователя')


def reset_password(request):
    return HttpResponse('В обработчике реализована логика сброса пароля пользователя')
