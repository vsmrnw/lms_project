from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse


class AuthAppTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание группы с правами "Ученик"
        cls.student_group = Group.objects.create(name='Ученик')
        cls.student_perms = Permission.objects.filter(
            content_type__app_label='learning',
            codename__in=['view', 'add_tracking'])
        cls.student_group.permissions.set(cls.student_perms)

    def setUp(self) -> None:
        self.user_valid_register_data = {
            'username': 'student',
            'email': 'student@example.com',
            'birthday': timezone.now().date(),
            'password1': 'student1234',
            'password2': 'student1234',
        }
        self.user_invalid_register_data = {
            'username': 'student@example.com',
            'birthday': timezone.now().date(),
            'password1': 'student1234',
            'password2': 'student4321',
        }
        self.user_login_data_with_remember = {
            'username': 'example@example.com',
            'password': 'student1234',
            'is_remember': 'on',
        }
        self.user_login_data_without_remember = {
            'username': 'example@example.com',
            'password': 'student1234',
            'is_remember': 'off',
        }
        self.invalid_login_data = {
            'username': 'example@example.com',
            'password': 'admin1234',
        }

        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin1234',
        )

        self.client = Client()
        self.register = reverse('register')
        self.login = reverse('user_login'),
        self.logout = reverse('logout'),
        self.index = reverse('index')

    def test_get_register_view(self):
        response = self.client.get(path=self.register, redirect=True, redirect_chain=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_post_register_view(self):
        response = self.client.post(path=self.register,
                                    data=self.user_valid_register_data, redirect=True, redirect_chain=True)
        self.assertEqual(response.status_code, 200)
