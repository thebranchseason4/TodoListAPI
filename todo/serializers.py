from rest_framework import serializers
from todo.models import TodoList


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TodoList
        fields = ('id', 'owner', 'list_name', 'creation_date')



