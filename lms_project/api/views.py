import django.db
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status, serializers
from rest_framework.authentication import BasicAuthentication, \
    TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, \
    ListCreateAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import AdminRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from auth_app.models import User
from learning.models import Course, Tracking
from .analytics import AnalyticReport
from .permissions import IsAuthor, IsStudent
from .serializers import (CourseSerializer, AnalyticSerializer,
                          UserSerializer, UserAdminSerializer,
                          StudentTrackingSerializer, AuthorTrackingSerializer)


class AnalyticViewSet(ViewSet):
    """
    Статистика по курам/-у
    """

    def list(self, request):
        courses = Course.objects.all()
        reports = [AnalyticReport(course=course) for course in courses]
        analytic_serializer = AnalyticSerializer(reports, many=False,
                                                 context={'request': request})
        return Response(data=analytic_serializer.data,
                        status=status.HTTP_200_OK)

    @action(methods=('get',), detail=False, url_path='(?P<course_id>[^/.]+)')
    def detail_analytic(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        reports = [AnalyticReport(course=course)]
        analytic_serializer = AnalyticSerializer(reports, many=False,
                                                 context={'request': request})
        return Response(data=analytic_serializer.data,
                        status=status.HTTP_200_OK)

    def get_view_name(self):
        return 'Аналитика'


class TrackingStudentViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'options',)
    serializer_class = StudentTrackingSerializer
    permission_classes = (IsAuthenticated, IsStudent,)
    lookup_field = 'lesson__course'
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        return Tracking.objects.filter(user=self.request.user)

    def get_object(self):
        tracking = self.get_queryset()
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return get_list_or_404(tracking, **filters)

    def retrieve(self, request, *args, **kwargs):
        tracking = self.get_object()
        tracking_serializer = self.get_serializer(tracking, many=True)
        return Response(tracking_serializer.data)

    @action(methods=('post',), detail=False, name='Запись на курс')
    def enroll(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user,
                               lesson=self.request.data[
                                   'lesson'])


class TrackingAuthorViewSet(TrackingStudentViewSet):
    http_method_names = ('get', 'post', 'patch', 'options',)
    serializer_class = AuthorTrackingSerializer
    permission_classes = (IsAuthenticated, IsAuthor,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('user__last_name', 'user__first_name', 'lesson__name',)

    def get_queryset(self):
        return Tracking.objects.filter(
            lesson__course__authors=self.request.user)

    def perform_create(self, serializer):
        data = self.request.data
        return serializer.save(user=User.objects.get(id=data['user']),
                               lesson=data['lesson'])

    @action(methods=('patch',), detail=False, name='Отметка о сдаче урока')
    def update_passed(self, request, *args, **kwargs):
        data = sorted(request.data, key=lambda x: int(x['id']))
        ids = list(map(lambda x: x['id'], data))
        instances = Tracking.objects.filter(id__in=ids).order_by('id')
        serializer = self.get_serializer(instances, data=data, many=True,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.update(serializer.instance, serializer.validated_data)


class UserForAdminView(ListCreateAPIView):
    name = 'Список пользователей LMS Edushka'
    serializer_class = UserAdminSerializer
    pagination_class = PageNumberPagination
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAdminUser,)
    renderer_classes = (AdminRenderer,)

    def get_queryset(self):
        return User.objects.all()


class CourseCreateView(CreateAPIView):
    name = 'Создать курс'
    serializer_class = CourseSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (BasicAuthentication,)

    def perform_create(self, serializer):
        serializer.save(authors=(self.request.user,))


class CourseDeleteView(RetrieveAPIView):
    name = 'Удалить курс'
    serializer_class = CourseSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'course_id'
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return Course.objects.all()


class CourseListAPIView(ListAPIView):
    name = 'Список курсов'
    description = 'Информация о всех курсах, размещенных на платформе Edushka'
    authentication_classes = (TokenAuthentication,)
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title', 'description', 'authors__first_name',
                     'authors__last_name', 'start_date',)
    ordering_fields = ('start_date', 'price',)
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
