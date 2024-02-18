from django.contrib import admin

# Register your models here.
from .models import Task, User, Pomodoro
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Pomodoro)