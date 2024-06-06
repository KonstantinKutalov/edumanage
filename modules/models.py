from django.db import models
from django.conf import settings
from users.models import NULLABLE


class Module(models.Model):
    number = models.IntegerField(verbose_name='Порядковый номер')
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, related_name='module')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ('number',)
