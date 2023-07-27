from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Course, Lesson, Tracking
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
    if request.user.is_anonymous:
        return redirect('login')
    else:
        is_existed = Tracking.objects.filter(user=request.user).exists()
        if is_existed:
            return HttpResponse(f'Вы уже записаны на данный курс')
        else:
            lessons = Lesson.objects.filter(course=course_id)
            records = [Tracking(lesson=lesson, user=request.user, passed=False) for lesson in lessons]
            Tracking.objects.bulk_create(records)
            return HttpResponse(f'Вы записаны на данный курс')


def index(request):
    courses = Course.objects.all()
    current_year = datetime.now().year
    return render(request, context={'courses': courses,
                                    'current_year': current_year},
                  template_name='index.html')