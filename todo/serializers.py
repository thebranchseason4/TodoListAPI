from rest_framework import serializers
from todo.models import Task
from todo.models import TodoList


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'list', 'title', 'description', 'date', 'priority', 'done')


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tasks = TaskSerializer(many=True, read_only=True)
    # TODO: implement create method to remove read only

    class Meta:
        model = TodoList
        fields = ('id', 'owner', 'list_name', 'date_created','tasks')
