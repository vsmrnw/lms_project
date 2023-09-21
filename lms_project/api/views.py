import django.db
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from auth_app.models import User
from learning.models import Course
from .analytics import AnalyticReport
from .serializers import CourseSerializer, AnalyticSerializer, UserSerializer


class CourseListAPIView(ListAPIView):
    name = 'Список курсов'
    description = 'Информация о всех курсах, размещенных на платформе Edushka'
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title', 'description', 'authors__first_name',
                     'authors__last_name', 'start_date', )
    ordering_fields = ('start_date', 'price', )
    ordering = 'title'

    def get_queryset(self):
        return Course.objects.all()


class CourseRetrieveAPIView(RetrieveAPIView):
    name = 'Курс'
    description = 'Получение курса по id, переданному в URL'
    serializer_class = CourseSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.all()


@api_view(['GET'])
def analytics(request):
    courses = Course.objects.all()
    reports = [AnalyticReport(course=course) for course in courses]
    analytic_serializer = AnalyticSerializer(reports, many=False,
                                             context={'request': request})
    return Response(data=analytic_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_serializer = UserSerializer(instance=users, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        try:
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.instance = user_serializer \
                    .save(user_serializer.validated_data)
                return Response(data=user_serializer.data,
                                status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(data=user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except django.db.IntegrityError:
            return Response(
                data={'email': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            return Response(data={'error': str(exception)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
