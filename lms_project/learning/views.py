from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Course, Lesson, Tracking, Review
from datetime import datetime
from .forms import CourseForm, ReviewForm, LessonForm, OrderByAndSearchForm
from django.urls import reverse


class MainView(ListView, FormView):
    template_name = 'index.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'

    form_class = OrderByAndSearchForm

    def get_queryset(self):
        queryset = MainView.queryset
        if {'search', 'price_order'} != self.request.GET.keys():
            return queryset
        else:
            search_query = self.request.GET.get('search')
            price_order_by = self.request.GET.get('price_order')
            filter = Q(title__icontains=search_query) | Q(
                description__icontains=search_query)
            queryset = queryset.filter(filter).order_by(price_order_by)
        return queryset

    def get_initial(self):
        initial = super(MainView, self).get_initial()
        initial['search'] = self.request.GET.get('search', '')
        initial['price_order'] = self.request.GET.get('price_order', 'title')
        return initial

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Course
    form_class = CourseForm

    permission_required = ('learning.add_course',)

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        with transaction.atomic():
            course = form.save(commit=False)
            course.author = self.request.user
            course.save()
            return super(CourseCreateView, self).form_valid(form)


class CourseDetailView(ListView):
    template_name = 'detail.html'
    context_object_name = 'lessons'
    pk_url_kwarg = 'course_id'

    def get(self, request, *args, **kwargs):
        views = request.session.setdefault('views', {})
        course_id = str(kwargs[CourseDetailView.pk_url_kwarg])
        count = views.get(course_id, 0)
        views[course_id] = count + 1
        request.session['views'] = views
        return super(CourseDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Lesson.objects.select_related('course').filter(course=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.select_related('user').filter(
            course=self.kwargs.get('course_id'))
        return context


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'create.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.change_course',)

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'delete.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.delete_course',)

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('index')


class LessonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.add_lesson', )

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.kwargs.get('course_id')})

    def get_form(self, form_class=None):
        form = super(LessonCreateView, self).get_form()
        form.fields['course'].queryset = Course.objects.filter(
            authors=self.request.user)
        return form


@transaction.atomic
@login_required
@permission_required('learning.add_tracking', raise_exception=True)
def enroll(request, course_id):
    is_existed = Tracking.objects.filter(user=request.user).exists()
    if is_existed:
        return HttpResponse(f'Вы уже записаны на данный курс')
    else:
        lessons = Lesson.objects.filter(course=course_id)
        records = [Tracking(lesson=lesson, user=request.user,
                            passed=False) for lesson in lessons]
        Tracking.objects.bulk_create(records)
        return HttpResponse(f'Вы записаны на данный курс')


@transaction.non_atomic_requests
@login_required
@permission_required('learning.add_review', raise_exception=True)
def review(request, course_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.errors:
            errors = form.errors[NON_FIELD_ERRORS]
            return render(request, 'review.html', {'form': form, 'errors': errors})
        if form.is_valid():
            data = form.cleaned_data
            Review.objects.create(content=data['content'],
                                  course=Course.objects.get(id=course_id),
                                  user=request.user)
        return redirect(reverse('detail', kwargs={'course_id': course_id}))
    else:
        form = ReviewForm()
        return render(request, 'review.html', {'form': form})


def add_booking(request, course_id):
    if request.method == 'POST':
        favourites = request.session.get('favourites', list())
        favourites.append(course_id)
        request.session['favourites'] = favourites
        request.session.modified = True

    return redirect(reverse('index'))


def remove_booking(request, course_id):
    if request.method == 'POST':
        request.session.get('favourites').remove(course_id)
        request.session.modified = True

    return redirect(reverse('index'))


class FavouriteView(MainView):

    def get_queryset(self):
        queryset = super(FavouriteView, self).get_queryset()
        ids = self.request.session.get('favourites', list())
        return queryset.filter(id__in=ids)
