from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from auth_app.functions import get_timestamp_path_user


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'student',
            'email': 'student@example.com',
            'birthday': timezone.now().date(),
            'password': 'student1234',
            'avatar': 'avatar.png',
        }
        get_user_model().objects.create_user(**self.user_data)

    def test_user_to_str(self):
        user = get_user_model().objects.first()
        self.assertEqual(str(user), f'Участник {self.user.first_name} '
                                    f'{self.user.last_name}: {self.user.email}')

    def test_path_from_avatar(self):
        user = get_user_model().objects.first()
        self.assertEqual(get_timestamp_path_user(user, self.user_data['avatar']),
                         'users/avatar.png')
