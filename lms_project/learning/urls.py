from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('create/', create, name='create'),
    path('delete/<int:course_id>', delete, name='delete'),
    re_path('^detail/(?P<course_id>[1-9])/$', CourseDetailView.as_view(), name='detail'),
    re_path('^enroll/(?P<course_id>[1-9]|1[0-5])/$', enroll, name='enroll'),
    path('', MainView.as_view(), name='index'),
]
