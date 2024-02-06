from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'done')
    list_filter = ('date', 'done')
    search_fields = ('title', 'date')