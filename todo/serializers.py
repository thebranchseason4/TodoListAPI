from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Tag
        fields = ('id', 'text', 'task')
