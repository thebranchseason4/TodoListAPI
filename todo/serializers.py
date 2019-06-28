from rest_framework import serializers
from todo.models import Task, PRIORITY_CHOICES
from datetime import datetime


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)
    date = serializers.DateTimeField(default=datetime.now())
    priority = serializers.ChoiceField(choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES[2])
    done = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Task.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance
