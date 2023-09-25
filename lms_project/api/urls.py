from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import analytics, users, CourseListAPIView, \
    CourseRetrieveAPIView, UserForAdminView

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>', CourseRetrieveAPIView.as_view(),
         name='courses_id'),
    path('analytics/', analytics, name='analytics'),
    path('users/', users, name='user'),
    # Authentication urls
    path('authentication/', include('rest_framework.urls')),
    path('generate-token/', obtain_auth_token, name='generate_token'),
    path('users-for-admin/', UserForAdminView.as_view(), name='users-for-admin'),
    ]
