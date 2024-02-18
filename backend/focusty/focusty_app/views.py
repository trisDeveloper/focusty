from rest_framework import generics
from .models import User, Task, Pomodoro
from .serializers import TaskSerializer, UserSerializer, PomodoroSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        serializer.save(user_id=user_id)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User does not exist'}, status=404)
        if password == user.password:
            print(user)
            return JsonResponse({'success': True, 'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }})

        else:
            return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    

class PomodoroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pomodoro.objects.all()
    serializer_class = PomodoroSerializer

from django.db.models.functions import TruncDate

class PomodoroListCreate(generics.ListCreateAPIView):
    serializer_class = PomodoroSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Pomodoro.objects.filter(user_id=user_id)\
            .values('date')\
            .annotate(minutes=Sum('minutes'))\
            .order_by('-date')

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        serializer.save(user_id=user_id)
