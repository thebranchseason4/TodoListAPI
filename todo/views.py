from django.contrib.auth.models import User
from rest_framework import viewsets

from todo.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
