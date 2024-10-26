# views.py
import uuid
from datetime import datetime
from rest_framework import generics
from .models import User, Task, Pomodoro
from .serializers import TaskSerializer, UserSerializer, PomodoroSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
from django.db.models import Count
from django.db.models import Sum
from .task_repeat import repeat_task


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Task.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]

        repeat_params = serializer.validated_data.get("repeatParameters", None)
        start_date = serializer.validated_data.get("date")
        if repeat_params:
            # Call repeat_task to generate dates based on repeat parameters
            dates = repeat_task(repeat_params, start_date)
            repeat_id = str(uuid.uuid4())
            for date_instance in dates:

                new_serializer = self.get_serializer(
                    data={
                        **serializer.validated_data,
                        "user": user_id,
                        "date": date_instance.date(),
                        "repeatId": repeat_id,
                    }
                )
                new_serializer.is_valid(raise_exception=True)
                new_serializer.save()
        else:
            # If no repeat, save the task as usual
            serializer.save(user_id=user_id)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    """def update(self, request, *args, **kwargs):
        instance = self.get_object()
        repeat_id = instance.repeatId
        this_or_all = request.data.get("thisOrAll", "this")

        if this_or_all == "this":
            return super().update(request, *args, **kwargs)
        elif this_or_all == "all" and repeat_id:
            # Update all tasks with the same repeatId
            tasks = Task.objects.filter(repeatId=repeat_id)
            for task in tasks:
                for key, value in request.data.items():
                    setattr(task, key, value)
                task.save()
            return Response({"status": "updated all tasks"}, status=status.HTTP_200_OK)"""


@api_view(["GET"])
def tasks_count(request, user_id):
    tasks_count_by_date = (
        Task.objects.filter(user_id=user_id)
        .values("date")
        .annotate(tasks_count=Count("id"))
    )

    return Response(tasks_count_by_date)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "User does not exist"}, status=404
            )
        if password == user.password:
            print(user)
            return JsonResponse(
                {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            )

        else:
            return JsonResponse(
                {"success": False, "message": "Invalid email or password"}, status=400
            )
    else:
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )


class PomodoroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pomodoro.objects.all()
    serializer_class = PomodoroSerializer


class PomodoroListCreate(generics.ListCreateAPIView):
    serializer_class = PomodoroSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return (
            Pomodoro.objects.filter(user_id=user_id)
            .values("date")
            .annotate(minutes=Sum("minutes"))
            .order_by("-date")
        )

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        serializer.save(user_id=user_id)
