from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny


class UserViewSet(ModelViewSet):
    """
    API-представление для модели User.

    **Доступ:**
    - Для создания пользователя доступен всем.
    - Для остальных действий доступен только администраторам.

    **Методы:**
    - **GET:** Получение списка пользователей (доступно только администраторам).
    - **POST:** Создание нового пользователя (доступно всем).
    - **GET (pk):** Получение информации о конкретном пользователе (доступно только администраторам).
    - **PUT (pk):** Обновление информации о пользователе (доступно только администраторам).
    - **DELETE (pk):** Удаление пользователя (доступно только администраторам).

    **Данные запроса:**
    - **Создание:**
        - `email` (str): Email пользователя.
        - `password` (str): Пароль пользователя.
        - `first_name` (str): Имя пользователя.
        - `last_name` (str): Фамилия пользователя.

    **Ответ:**
    - **Создание:**
        - `201 Created`: Пользователь успешно создан.
        - `400 Bad Request`: Неверные данные в запросе.
    - **Прочие действия:**
        - `200 OK`: Действие выполнено успешно.
        - `400 Bad Request`: Неверные данные в запросе.
        - `403 Forbidden`: У пользователя нет прав на выполнение действия.
        - `404 Not Found`: Пользователь не найден.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Сохранение пользователя в базу данных
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        # Настройка прав доступа:
        # - Для создания пользователя доступен всем
        # - Для остальных действий доступен только администраторам
        if self.action != 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]