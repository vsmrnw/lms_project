from django.urls import path
from api.views import courses, courses_id, analytics

urlpatterns = [
    path('courses/', courses, name='courses'),
    path('courses/<int:course_id>', courses_id, name='courses_id'),
    path('analytics/', analytics, name='analytics'),
]