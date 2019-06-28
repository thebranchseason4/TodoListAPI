from django.contrib.auth.models import User
from rest_framework import viewsets

from todo.models import Task
from todo.models import TodoList
from todo.serializers import TaskSerializer
from todo.serializers import TodoListSerializer
from todo.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
