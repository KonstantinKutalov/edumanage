from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission

NULLABLE = {'blank': True, 'null': True}


# Менеджер пользователей, расширяющий стандартный менеджер Django
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError("Поле 'email' обязательно для заполнения.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает обычного пользователя.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь 'is_staff=True'.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь 'is_superuser=True'.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя"""
    objects = UserManager()

    # Отключаем поле username
    username = None

    # Email пользователя (уникальный)
    email = models.EmailField(unique=True, verbose_name='Email')

    # Имя и фамилия пользователя
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')

    # Настройка обратных связей для групп и разрешений
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Разрешения',
        related_name='custom_user_set'
    )

    # Устанавливаем email как имя пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'