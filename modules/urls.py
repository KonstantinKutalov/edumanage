from django.urls import path

from modules.views import ModulesCreateAPIView, ModulesListAPIView, ModulesRetrieveAPIView, ModulesUpdateAPIView, \
    ModulesDestroyAPIView

urlpatterns = [
    # Создание модуля
    path('modules/create/', ModulesCreateAPIView.as_view(), name='module_new'),
    # Список модулей
    path('modules/', ModulesListAPIView.as_view(), name='modules_all'),
    # Просмотр модуля
    path('modules/<int:pk>/', ModulesRetrieveAPIView.as_view(), name='module_details'),
    # Обновление модуля
    path('modules/update/<int:pk>/', ModulesUpdateAPIView.as_view(), name='module_edit'),
    # Удаление модуля
    path('modules/delete/<int:pk>/', ModulesDestroyAPIView.as_view(), name='module_remove'),
]