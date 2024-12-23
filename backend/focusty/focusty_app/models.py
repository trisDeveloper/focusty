# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from .task_repeat import repeat_task


class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    country = models.CharField(max_length=100, null=True, blank=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True)
    repeatId = models.CharField(max_length=255, blank=True, null=True)
    repeatParameters = models.JSONField(null=True, blank=True)
    done = models.BooleanField(default=False)
    color = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Pomodoro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pomodoro")
    date = models.DateField(auto_now_add=True)
    minutes = models.IntegerField(default=0)
