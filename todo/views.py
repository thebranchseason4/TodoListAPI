# Create your views here.
from rest_framework import viewsets

from todo.models import TodoList
from todo.serializers import TodoListSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
