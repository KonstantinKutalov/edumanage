from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from modules.models import Module

User = get_user_model()


class ModulesAPITest(TestCase):
    """Тесты для API модулей."""

    def setUp(self):
        """Настройка для каждого теста."""
        self.client = APIClient()  # Создаем клиента API
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')  # Создаем тестового пользователя
        self.client.force_authenticate(user=self.user)  # Аутентифицируем клиента с помощью тестового пользователя
        self.module_data = {
            'number': 1,
            'name': 'Test Module',
            'description': 'Test Description'
        }  # Данные для создания тестового модуля

    def test_create_module(self):
        """Проверка создания модуля."""
        response = self.client.post('/modules/create/', self.module_data, format='json')  # Отправляем POST-запрос на создание модуля
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем, что код ответа 201 (Создано)
        self.assertEqual(Module.objects.count(), 1)  # Проверяем, что в базе данных появился 1 модуль
        self.assertEqual(Module.objects.get().name, 'Test Module')  # Проверяем, что имя созданного модуля соответствует отправленным данным

    def test_list_modules(self):
        """Проверка получения списка модулей."""
        Module.objects.create(number=1, name='Module 1', owner=self.user)  # Создаем два тестовых модуля
        Module.objects.create(number=2, name='Module 2', owner=self.user)
        response = self.client.get('/modules/')  # Отправляем GET-запрос на получение списка модулей
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что код ответа 200 (ОК)
        self.assertEqual(len(response.data['results']), 2)  # Проверяем, что в ответе два модуля

    def test_retrieve_module(self):
        """Проверка получения информации о конкретном модуле."""
        module = Module.objects.create(number=1, name='Module 1', owner=self.user)  # Создаем тестовый модуль
        response = self.client.get(f'/modules/{module.id}/')  # Отправляем GET-запрос на получение информации о модуле
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что код ответа 200 (ОК)
        self.assertEqual(response.data['name'], 'Module 1')  # Проверяем, что в ответе имя модуля соответствует созданному

    def test_update_module(self):
        """Проверка обновления модуля."""
        module = Module.objects.create(number=1, name='Module 1', owner=self.user)  # Создаем тестовый модуль
        update_data = {'number': 2, 'name': 'Updated Module', 'description': 'Updated Description'}  # Данные для обновления модуля
        response = self.client.put(f'/modules/update/{module.id}/', update_data, format='json')  # Отправляем PUT-запрос на обновление модуля
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем, что код ответа 200 (ОК)
        module.refresh_from_db()  # Обновляем данные модуля из базы данных
        self.assertEqual(module.number, 2)  # Проверяем, что номер модуля обновился
        self.assertEqual(module.name, 'Updated Module')  # Проверяем, что имя модуля обновилось
        self.assertEqual(module.description, 'Updated Description')  # Проверяем, что описание модуля обновилось

    def test_destroy_module(self):
        """Проверка удаления модуля."""
        module = Module.objects.create(number=1, name='Module 1', owner=self.user)  # Создаем тестовый модуль
        response = self.client.delete(f'/modules/delete/{module.id}/')  # Отправляем DELETE-запрос на удаление модуля
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверяем, что код ответа 204 (Нет содержимого)
        self.assertEqual(Module.objects.count(), 0)  # Проверяем, что модуль удален из базы данных

    def test_permissions(self):
        """Проверка прав доступа."""
        another_user = User.objects.create_user(email='anotheruser@example.com', password='anotherpass')  # Создаем тестового пользователя
        module = Module.objects.create(number=1, name='Module 1', owner=another_user)  # Создаем модуль, принадлежащий другому пользователю

        # Пытаемся обновить модуль, принадлежащий другому пользователю
        update_data = {'name': 'Should Not Update'}  # Данные для обновления модуля
        response = self.client.put(f'/modules/update/{module.id}/', update_data, format='json')  # Отправляем PUT-запрос на обновление модуля
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Проверяем, что код ответа 404 (Не найдено)

        # Пытаемся удалить модуль, принадлежащий другому пользователю
        response = self.client.delete(f'/modules/delete/{module.id}/')  # Отправляем DELETE-запрос на удаление модуля
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Проверяем, что код ответа 404 (Не найдено)