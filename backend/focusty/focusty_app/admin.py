from django.contrib import admin

# Register your models here.
from .models import Task, User
admin.site.register(Task)
admin.site.register(User)