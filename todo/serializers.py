from django.contrib.auth.models import User
from rest_framework import serializers
from todo.models import Task
from todo.models import TodoList


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
