from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny


class UserViewSet(ModelViewSet):
    """
    API-представление для модели User.
    Для создания пользователя необходимо указать 'email' и 'password'.
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