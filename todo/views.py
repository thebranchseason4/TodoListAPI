from django.contrib.auth.models import User
from rest_framework import viewsets

from todo.models import TodoList, Tag, Task
from todo.serializers import TodoListSerializer, TagSerializer, TaskSerializer
from todo.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
