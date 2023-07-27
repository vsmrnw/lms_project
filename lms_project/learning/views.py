from django.http import HttpResponse
from django.shortcuts import render
from .models import Course
from datetime import datetime

def create(request):
    return HttpResponse('Страница создания нового курса')


def delete(request, course_id):
    return HttpResponse(f'Страница для удаления {course_id} курса')


def detail(request, course_id):
    return HttpResponse(f'Страница информации о {course_id} курсе')


def enroll(request, course_id):
    return HttpResponse(f'Страница для записи на курс {course_id}')


def index(request):
    courses = Course.objects.all()
    current_year = datetime.now().year
    return render(request, context={'courses': courses,
                                    'current_year': current_year},
                  template_name='index.html')