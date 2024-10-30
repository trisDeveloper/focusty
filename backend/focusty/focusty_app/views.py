# views.py
import uuid, json
from rest_framework import generics
from .models import User, Task, Pomodoro
from .serializers import TaskSerializer, UserSerializer, PomodoroSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken


from django.db.models import Count, Sum
from .task_repeat import repeat_task


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            return JsonResponse(
                {"error": "You do not have permission to access this data."}
            )
        return obj


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        user = self.get_user_from_response(response.data)

        if user:
            # Hash the password securely
            user.set_password(user.password)
            user.save()
            token = RefreshToken.for_user(user)
            response.data["access"] = str(token.access_token)
            response.data["refresh"] = str(token)
        return response

    def get_user_from_response(self, data):
        try:
            user_id = data.get("id")
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


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

        if user.check_password(password):
            # Generate token
            token = RefreshToken.for_user(user)

            return JsonResponse(
                {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "access": str(token.access_token),
                    "refresh": str(token),
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

    def perform_update(self, serializer):
        task = self.get_object()
        repeat_id = task.repeatId
        update_data = serializer.validated_data
        update_scope = self.request.data.get("thisOrAll", "this")  # "all" or "this"
        repeat_params = update_data.get("repeatParameters", None)

        # If updating a repeat series
        if repeat_id:
            if update_scope == "all":
                # Removing repeat settings if `repeatParameters` is None
                if repeat_params is None:
                    task.repeatId = None
                    task.repeatParameters = None
                    task.save()
                    Task.objects.filter(repeatId=repeat_id).delete()

                else:
                    # Update all tasks in the series with new repeat parameters
                    repeat_start_date = (
                        Task.objects.filter(repeatId=repeat_id).earliest("date").date
                    )
                    Task.objects.filter(repeatId=repeat_id).delete()
                    new_dates = repeat_task(repeat_params, repeat_start_date)

                    # Recreate tasks with updated repeat parameters
                    for date in new_dates:
                        new_task_data = {
                            **update_data,
                            "user": task.user_id,
                            "date": date.date(),
                            "repeatId": repeat_id,
                        }
                        serializer_class = self.get_serializer(data=new_task_data)
                        serializer_class.is_valid(raise_exception=True)
                        serializer_class.save()
            else:
                # Update only the selected task
                if repeat_params is not None and repeat_params != task.repeatParameters:
                    # New repeat series with updated repeatParameters for this task only
                    new_repeat_id = str(uuid.uuid4())
                    start_date = task.date
                    Task.objects.filter(id=task.id).delete()
                    # Generate repeated instances
                    new_dates = repeat_task(repeat_params, start_date)
                    for date in new_dates:
                        new_task_data = {
                            **update_data,
                            "user": task.user_id,
                            "date": date.date(),
                            "repeatId": new_repeat_id,
                        }
                        serializer_class = self.get_serializer(data=new_task_data)
                        serializer_class.is_valid(raise_exception=True)
                        serializer_class.save()
                else:
                    for field, value in update_data.items():
                        setattr(task, field, value)

                    # Set repeat fields to None
                    task.repeatId = None
                    task.repeatParameters = None

                    # Save the task with all changes
                    task.save()

        # If the task is not currently repeated but needs to be set as repeated
        elif repeat_params:
            # Assign a new repeatId for the new repeat series
            new_repeat_id = str(uuid.uuid4())
            start_date = task.date
            Task.objects.filter(id=task.id).delete()
            # Generate repeated instances
            new_dates = repeat_task(repeat_params, start_date)
            for date in new_dates:
                new_task_data = {
                    **update_data,
                    "user": task.user_id,
                    "date": date.date(),
                    "repeatId": new_repeat_id,
                }
                serializer_class = self.get_serializer(data=new_task_data)
                serializer_class.is_valid(raise_exception=True)
                serializer_class.save()

        else:
            # If no repeat action is needed, update the task as usual
            serializer.save()

    def perform_destroy(self, instance):
        repeat_id = instance.repeatId
        delete_scope = self.request.data.get("thisOrAll", "this")

        if repeat_id:
            if delete_scope == "all":
                # Delete all tasks in the repeat series
                Task.objects.filter(repeatId=repeat_id).delete()
            else:
                # Delete just this specific task
                instance.delete()
        else:
            # If the task is not repeated, just delete it
            instance.delete()


@api_view(["GET"])
def tasks_count(request, user_id):
    tasks_count_by_date = (
        Task.objects.filter(user_id=user_id)
        .values("date")
        .annotate(tasks_count=Count("id"))
    )

    return Response(tasks_count_by_date)


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
