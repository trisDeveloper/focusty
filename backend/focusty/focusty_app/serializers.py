from rest_framework import serializers
from .models import User, Task, Pomodoro

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class PomodoroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pomodoro
        fields = ['date', 'minutes']