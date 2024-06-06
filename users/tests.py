# Тесты для моделей и сериализаторов
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer


class ModuleTest(TestCase):
    """
    Тесты для модели User.
    """

    def setUp(self):
        # Создание тестового пользователя
        User.objects.create(
            email='test@test.ru',
            first_name='Test',
            password='test'
        )

    def test_user_first_name(self):
        # Проверка правильности сохранения имени пользователя
        module = User.objects.get(email='test@test.ru')
        self.assertEqual(module.first_name, 'Test')


class UserSerializerTest(TestCase):
    """
    Тесты для сериализатора UserSerializer.
    """

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create(
            email='test@test.ru',
            password='test',
            first_name='Test',
            last_name='Testov'
        )

        # Создание сериализатора
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        # Проверка, содержит ли сериализатор ожидаемые поля
        data = self.serializer.data
        self.assertEqual(set(data.keys()),
                         set(['email', 'first_name', 'last_name', 'qty_modules']))


class UserCreateSerializerTest(TestCase):
    """
    Тесты для сериализатора UserCreateSerializer.
    """

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create(
            email='test@test.ru',
            password='test',
        )

        # Создание сериализатора
        self.serializer = UserCreateSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        # Проверка, содержит ли сериализатор ожидаемые поля
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['email', 'password', 'first_name', 'last_name']))


class UserTestCase(APITestCase):
    """
    Тесты для API-представления пользователя.
    """

    def setUp(self):
        # Создание тестового суперпользователя
        self.user = User.objects.create(email='test@test.com', is_staff=True, is_superuser=True)
        self.user.set_password('1234')
        self.user.save()

        # Получение токена доступа
        response = self.client.post(
            '/users/token/',
            {'email': 'test@test.com', 'password': "1234"}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Тестовые данные для создания пользователя
        self.data = {
            'email': 'test@example.com',
            'password': 'test',
            'first_name': 'Test',
            'last_name': 'Testov'
        }

    def test_create_user(self):
        # Проверка создания пользователя
        response = self.client.post(
            '/users/user/',
            self.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'email': 'test@example.com',
                'password': 'test',
                'first_name': 'Test',
                'last_name': 'Testov',
            }
        )

    def test_list_users(self):
        # Проверка получения списка пользователей
        response = self.client.get('/users/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    'email': 'test@test.com',
                    'first_name': '',
                    'last_name': '',
                    'qty_modules': 0,
                }
            ]
        )

    def test_retrieve_user(self):
        # Проверка получения информации о пользователе по идентификатору
        self.test_create_user()
        pk = User.objects.all().latest('pk').pk
        response = self.client.get(f'/users/user/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'Testov',
                'qty_modules': 0,
            }
        )

    def test_update_user(self):
        # Проверка обновления информации о пользователе
        self.test_create_user()
        pk = User.objects.all().latest('pk').pk
        response = self.client.patch(f'/users/user/{pk}/', {'first_name': 'Test1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'email': 'test@example.com',
                'first_name': 'Test1',
                'last_name': 'Testov',
                'qty_modules': 0,
            }
        )

    def test_destroy_user(self):
        # Проверка удаления пользователя
        self.test_create_user()
        pk = User.objects.all().latest('pk').pk
        response = self.client.delete(f'/users/user/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
