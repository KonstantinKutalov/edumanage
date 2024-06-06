from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from modules.models import Module
from modules.pagination import ModulesPaginator
from modules.serializers import ModuleSerializer


class ModulesCreateAPIView(generics.CreateAPIView):
    """Представление для создания модуля"""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_module = serializer.save()
        new_module.owner = self.request.user
        new_module.save()


class ModulesListAPIView(generics.ListAPIView):
    """Представление для получения списка модулей"""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulesPaginator


class ModulesRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для получения одного модуля по id"""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]


class ModulesUpdateAPIView(generics.UpdateAPIView):
    """Представление для редактирования модуля по id"""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)


class ModulesDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления модуля по id"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)
