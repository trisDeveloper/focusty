from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(4)])
    join_date = models.DateField(auto_now_add=True)
    birthday = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True)
    done = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Pomodoro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoro')
    date = models.DateField(auto_now_add=True)
    minutes = models.IntegerField(default=0)