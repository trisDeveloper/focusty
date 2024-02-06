from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskListCreateView, TaskUpdateView
router = DefaultRouter()
router.register(r'tasks', TaskListCreateView)
urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
]
