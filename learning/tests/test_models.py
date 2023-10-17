from django.test import TestCase
from learning.models import Course, Lesson


class LearningModelsTestCase(TestCase):
    fixtures = ['test_data.json']

    def test_course_to_str(self):
        course = Course.objects.get(title='Djnago Framework')
        self.assertEqual(str(course), f'{course.title}')

    def test_lesson_to_str(self):
        lesson = Lesson.objects.get(name='Установка Django')
        self.assertEqual(str(lesson), f'{lesson.course.title}: Урок '
                                      f'{lesson.name}')