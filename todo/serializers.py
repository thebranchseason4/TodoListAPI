from django.contrib.auth.models import User
from rest_framework import serializers

from todo.models import TodoList


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TodoList
        fields = ('id', 'owner', 'list_name', 'creation_date')


class UserSerializer(serializers.ModelSerializer):
    # user fields: 'id', 'first_name', 'last_name', 'email', 'password'
    class Meta:
        model = User
        fields = ('id', 'username', 'lists')
