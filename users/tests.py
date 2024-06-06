from django.test import TestCase
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer


class UserTest(TestCase):
    """
    Тесты для модели User.
    """

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create(
            email='test@test.ru',
            first_name='Test',
            password='test'
        )

    def test_user_first_name(self):
        # Проверка правильности сохранения имени пользователя
        user = User.objects.get(email='test@test.ru')
        self.assertEqual(user.first_name, 'Test')


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
        self.assertEqual(set(data.keys()), set(['email', 'first_name', 'last_name', 'module_count']))


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
