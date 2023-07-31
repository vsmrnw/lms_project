from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Course, Lesson, Tracking
from datetime import datetime



class MainView(ListView):
    template_name = 'index.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


class CourseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(course=self.kwargs.get('course_id'))
        return context

def create(request):
    if request.method == 'POST':
        data = request.POST
        Course.objects.create(title=data['title'], author=request.user,
                              description=data['description'], start_date=data['start_date'],
                              duration=data['duration'], price=data['price'],
                              count_lessons=data['count_lessons'])
        return redirect('index')
    else:
        return render(request, 'create.html')


def delete(request, course_id):
    Course.objects.get(id=course_id).delete()
    return redirect('index')


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
            records = [Tracking(lesson=lesson, user=request.user,
                                passed=False) for lesson in lessons]
            Tracking.objects.bulk_create(records)
            return HttpResponse(f'Вы записаны на данный курс')
