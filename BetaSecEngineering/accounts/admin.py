from django.contrib import admin

from .models import LabAccount


@admin.register(LabAccount)
class LabAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_name')
    search_fields = ('username', 'display_name')
