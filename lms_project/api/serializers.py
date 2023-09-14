from rest_framework.serializers import ModelSerializer
from learning.models import Course
from auth_app.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.natural_key()}'


class CourseSerializer(ModelSerializer):
    authors = UserSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
