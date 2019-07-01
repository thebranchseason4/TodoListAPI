from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

VERY_LOW = 1
LOW = 2
MEDIUM = 3
HIGH = 4
TOP = 5

PRIORITY_CHOICES = (
    (VERY_LOW, "Very Low Priority"),
    (LOW, "Low Priority"),
    (MEDIUM, "Medium Priority"),
    (HIGH, "High Priority"),
    (TOP, "Top Priority"),
)


class TodoList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='lists', null=True)
    list_name = models.CharField(max_length=255, default="")
    date_created = models.DateTimeField('creation date', default=datetime.now())


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date = models.DateTimeField('date created', default=timezone.now())
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=MEDIUM)
    done = models.BooleanField(default=False)
    list = models.ForeignKey('TodoList', related_name="tasks", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-priority',)


class Tag(models.Model):
    pass
