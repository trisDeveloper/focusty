# urls.py
from django.urls import path
from .views import (
    UserList,
    UserDetail,
    TaskListCreate,
    TaskDetail,
    login_view,
    PomodoroListCreate,
    PomodoroDetail,
    tasks_count,
)

urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    path("users/<int:user_id>/tasks/", TaskListCreate.as_view()),
    path("users/<int:user_id>/tasks/<int:pk>/", TaskDetail.as_view()),
    path("users/<int:user_id>/tasks/all/", tasks_count, name="tasks count"),
    path("login/", login_view, name="login"),
    path("users/<int:user_id>/pomodoros/", PomodoroListCreate.as_view()),
    path("users/<int:user_id>/pomodoros/<int:pk>/", PomodoroDetail.as_view()),
]
