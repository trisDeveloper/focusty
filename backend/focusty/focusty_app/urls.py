from django.urls import path
from .views import UserList, UserDetail, TaskListCreate, TaskDetail

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:user_id>/tasks/', TaskListCreate.as_view()),
    path('users/<int:user_id>/tasks/<int:pk>/', TaskDetail.as_view()),
]