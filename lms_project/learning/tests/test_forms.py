from django.forms.utils import ValidationError
from django.test import TestCase
from learning.forms import LessonForm
from learning.models import Course


class LearningFormTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.data = {
            'course': Course.objects.get(title='OSINT').id,
            'name': 'Пример конкурентного OSINT',
            'preview': 'В настоящее время – OSINT (Open Search INTelligence) является '
                       'основной технологией добычи данных. ОСИНТ используется для '
                       'поиска информации как в видимой части интернета: социальные сети, '
                       'блог площадки, электронные СМИ, доски объявлений, площадки для '
                       'поиска работы и т.п., так и в невидимой – глубинном интернете '
                       '(Deep Web, Dark Web): форумы, базы данных, LeakInt и т.п. '
                       'Даже государственные разведки, в 80% своей деятельности '
                       'черпают свои данные методами OSINT.'
        }

    def test_lesson_form_preview_length_error(self):
        form = LessonForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage('Слишком длинное описание! '
                                 'Сокртатие до 200 символов')