from django.contrib import admin

from modules.models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'description', 'owner')
    list_filter = ('owner',)
    search_fields = ('name',)
