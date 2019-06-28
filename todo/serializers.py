from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # user fields: 'id', 'first_name', 'last_name', 'email', 'password'
    class Meta:
        model = User
        fields = ('id', 'username', 'lists')
