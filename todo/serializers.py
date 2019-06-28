from rest_framework import serializers
from todo.models import TodoList
from .models import Tag


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TodoList
        fields = ('id', 'owner', 'list_name', 'creation_date')


class TagSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Tag
        fields = ('id', 'text', 'task')
