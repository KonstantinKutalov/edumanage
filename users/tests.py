from django.test import TestCase
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.test import TransactionTestCase


class UserTest(TransactionTestCase):
    """
    Тесты для модели User.
    """

    @classmethod
    def setUpTestData(cls):
        #  Создайте разрешения и группы здесь
        content_type = ContentType.objects.get_for_model(User)
        Permission.objects.create(
            name='Can add user',
            codename='add_user',
            content_type=content_type
        )
        Group.objects.create(name='TestGroup')

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create(
            email='test@test.ru',
            first_name='Test',
            password=make_password('test')
        )

    def test_user_first_name(self):
        # Проверка правильности сохранения имени пользователя
        user = User.objects.get(email='test@test.ru')
        self.assertEqual(user.first_name, 'Test')

    def test_create_user_with_valid_data(self):
        # Проверка создания пользователя с валидными данными
        user = User.objects.create_user(
            email='newuser@example.com',
            password='testpassword',
            first_name='New',
            last_name='User'
        )
        self.assertIsNotNone(user.pk)  # Проверка, что пользователь создан
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')

    def test_create_user_with_invalid_email(self):
        # Проверка создания пользователя с невалидным email
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',  # Пустой email
                password='testpassword',
                first_name='Test',
                last_name='User'
            )

    def test_create_superuser(self):
        # Проверка создания суперпользователя
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_unique_email(self):
        # Проверка уникальности email
        User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        with self.assertRaises(Exception):
            # Попытка создания второго пользователя с таким же email
            User.objects.create_user(
                email='test@example.com',
                password='testpassword'
            )

    def test_set_password(self):
        # Проверка хеширования пароля
        self.user.set_password('newpassword')
        self.assertNotEqual(self.user.password, 'newpassword')  # Проверка, что пароль захеширован

    def test_check_password(self):
        # Проверка корректного сравнения пароля
        self.assertTrue(self.user.check_password('test'))  # Изначальный пароль
        self.assertFalse(self.user.check_password('wrongpassword'))  # Неверный пароль

    def test_add_remove_group(self):
        # Проверка добавления и удаления пользователя из группы
        group = Group.objects.create(name='TestGroup')
        self.user.groups.add(group)
        self.assertIn(group, self.user.groups.all())
        self.user.groups.remove(group)
        self.assertNotIn(group, self.user.groups.all())

    def test_add_remove_permission(self):
        # Проверка добавления и удаления разрешений для пользователя
        permission = Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(permission)
        self.assertIn(permission, self.user.user_permissions.all())
        self.user.user_permissions.remove(permission)
        self.assertNotIn(permission, self.user.user_permissions.all())


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

    def test_serialize_user(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['email'], 'test@test.ru')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'Testov')
        # ... (проверка остальных полей)

    def test_validate_create_user(self):
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_create_user_invalid_data(self):
        data = {
            'email': '',  # Пустой email
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['email'][0], 'This field may not be blank.')


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
