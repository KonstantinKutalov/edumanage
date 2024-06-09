from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from modules.models import Module
from modules.pagination import ModulesPaginator
from modules.serializers import ModuleSerializer


class ModulesCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового модуля.

    **Доступ:**
    - Доступно только авторизованным пользователям.

    **Метод:**
    - POST

    **Данные запроса:**
    - `number` (int): Порядковый номер модуля.
    - `name` (str): Название модуля.
    - `description` (str, optional): Описание модуля.

    **Ответ:**
    - `201 Created`: Модуль успешно создан.
    - `400 Bad Request`: Неверные данные в запросе.
    """
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_module = serializer.save()
        new_module.owner = self.request.user
        new_module.save()


class ModulesListAPIView(generics.ListAPIView):
    """
    Представление для получения списка модулей.

    **Доступ:**
    - Доступно всем пользователям.

    **Метод:**
    - GET

    **Ответ:**
    - `200 OK`: Список модулей.
    """
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulesPaginator


class ModulesRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения одного модуля по ID.

    **Доступ:**
    - Доступно только авторизованным пользователям.

    **Метод:**
    - GET

    **Параметры пути:**
    - `pk` (int): ID модуля.

    **Ответ:**
    - `200 OK`: Информация о модуле.
    - `404 Not Found`: Модуль не найден.
    """
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]


class ModulesUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для редактирования модуля по ID.

    **Доступ:**
    - Доступно только авторизованным пользователям, являющимся владельцами модуля.

    **Метод:**
    - PUT

    **Параметры пути:**
    - `pk` (int): ID модуля.

    **Данные запроса:**
    - `number` (int): Порядковый номер модуля.
    - `name` (str): Название модуля.
    - `description` (str, optional): Описание модуля.

    **Ответ:**
    - `200 OK`: Модуль успешно обновлен.
    - `400 Bad Request`: Неверные данные в запросе.
    - `403 Forbidden`: У пользователя нет прав на редактирование модуля.
    - `404 Not Found`: Модуль не найден.
    """
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)


class ModulesDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления модуля по ID.

    **Доступ:**
    - Доступно только авторизованным пользователям, являющимся владельцами модуля.

    **Метод:**
    - DELETE

    **Параметры пути:**
    - `pk` (int): ID модуля.

    **Ответ:**
    - `204 No Content`: Модуль успешно удален.
    - `403 Forbidden`: У пользователя нет прав на удаление модуля.
    - `404 Not Found`: Модуль не найден.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)