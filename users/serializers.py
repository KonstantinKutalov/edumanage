from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    module_count = serializers.SerializerMethodField()

    def get_module_count(self, instance):
        return instance.module.count()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'module_count')


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового пользователя.
    """
    def create(self, validated_data):
        # Создание нового пользователя
        instance = User.objects.create_user(**validated_data)
        return instance

    class Meta:
        model = User
        # Поля, используемые при создании пользователя
        fields = ('email', 'password', 'first_name', 'last_name')