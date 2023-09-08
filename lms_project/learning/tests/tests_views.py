from django.test import TestCase, Client
from django.urls import reverse


class LearningViewTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.client = Client()
        self.index = reverse('index')
        self.create = reverse('create')
        self.tracking = reverse('tracking')

    def test_get_index_view(self):
        response = self.client.get(self.index)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['courses']), 5)

    def test_get_index_view_by_page(self):
        response = self.client.get(self.index, data={'page': 2})
        self.assertEqual(len(response.context['courses']), 1)
