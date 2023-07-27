from django.http import HttpResponse
from django.shortcuts import render
from .models import Course, Lesson
from datetime import datetime

def create(request):
    return HttpResponse('Страница создания нового курса')


def delete(request, course_id):
    return HttpResponse(f'Страница для удаления {course_id} курса')


def detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course_id)
    context = {'course': course, 'lessons': lessons}
    return render(request, 'detail.html', context)


def enroll(request, course_id):
    return HttpResponse(f'Страница для записи на курс {course_id}')


def index(request):
    courses = Course.objects.all()
    current_year = datetime.now().year
    return render(request, context={'courses': courses,
                                    'current_year': current_year},
                  template_name='index.html')