# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from todo.models import Task
from todo.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


