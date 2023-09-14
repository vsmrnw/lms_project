from django.db.models import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from learning.models import Course
from .serializers import CourseSerializer


@api_view(['GET'])
def courses(request):
    courses = Course.objects.all()
    courses_serializer = CourseSerializer(instance=courses, many=True)
    return Response(data=courses_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def courses_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course_serializer = CourseSerializer(instance=course, many=False)
        return Response(data=course_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as exception:
        return Response(data={'error': 'Запрашиваемый Курс отсуствует в системе'},
                        status=status.HTTP_404_NOT_FOUND)