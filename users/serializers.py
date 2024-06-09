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

    class Meta:
        model = User
        # Поля, используемые при создании пользователя
        fields = ('email', 'password', 'first_name', 'last_name')
        # При сериализации объекта, поле пароля будет учитываться только при создании или обновлении
        # объекта, но не будет включено в представление объекта при его получении.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = User.objects.create(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
