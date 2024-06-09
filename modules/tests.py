from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from modules.models import Module

User = get_user_model()


class ModulesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.module_data = {
            'number': 1,
            'name': 'Test Module',
            'description': 'Test Description'
        }

    def test_create_module(self):
        response = self.client.post('/modules/create/', self.module_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.get().name, 'Test Module')

    def test_list_modules(self):
        Module.objects.create(number=1, name='Module 1', owner=self.user)
        Module.objects.create(number=2, name='Module 2', owner=self.user)

        response = self.client.get('/modules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_module(self):
        module = Module.objects.create(number=1, name='Module 1', owner=self.user)
        response = self.client.get(f'/modules/{module.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Module 1')

    def test_update_module(self):
        module = Module.objects.create(number=1, name='Module 1', owner=self.user)
        update_data = {'number': 2, 'name': 'Updated Module', 'description': 'Updated Description'}

        response = self.client.put(f'/modules/update/{module.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        module.refresh_from_db()
        self.assertEqual(module.number, 2)
        self.assertEqual(module.name, 'Updated Module')
        self.assertEqual(module.description, 'Updated Description')

    def test_destroy_module(self):
        module = Module.objects.create(number=1, name='Module 1', owner=self.user)
        response = self.client.delete(f'/modules/delete/{module.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.count(), 0)

    def test_permissions(self):
        another_user = User.objects.create_user(email='anotheruser@example.com', password='anotherpass')
        module = Module.objects.create(number=1, name='Module 1', owner=another_user)

        # Try to update another user's module
        update_data = {'name': 'Should Not Update'}
        response = self.client.put(f'/modules/update/{module.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete another user's module
        response = self.client.delete(f'/modules/delete/{module.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
