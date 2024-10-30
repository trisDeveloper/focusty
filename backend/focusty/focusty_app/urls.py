# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserList,
    UserDetail,
    TaskListCreate,
    TaskDetail,
    login_view,
    RegisterView,
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
    path("register/", RegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/<int:user_id>/pomodoros/", PomodoroListCreate.as_view()),
    path("users/<int:user_id>/pomodoros/<int:pk>/", PomodoroDetail.as_view()),
]
