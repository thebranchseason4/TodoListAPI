from rest_framework import viewsets
from todo.models import Task
from todo.serializers import TaskSerializer
from todo.models import TodoList
from todo.serializers import TodoListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
