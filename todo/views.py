from django.contrib.auth.models import User
from rest_framework import viewsets

from todo.models import TodoList
from todo.serializers import TodoListSerializer
from todo.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
