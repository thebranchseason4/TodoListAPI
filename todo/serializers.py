from django.contrib.auth.models import User
from rest_framework import serializers

from todo.models import Task
from todo.models import TodoList
from .models import Tag, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'list', 'title', 'description', 'date', 'priority', 'done')


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = ('id', 'owner', 'list_name', 'date_created', 'tasks')


class TagSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), many=True)

    class Meta:
        model = Tag
        fields = ('id', 'text', 'task')


class UserSerializer(serializers.ModelSerializer):
    # user fields: 'id', 'first_name', 'last_name', 'email', 'password'
    lists = TodoListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'lists')