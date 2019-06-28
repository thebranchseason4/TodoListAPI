from datetime import datetime

from django.db import models

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
    pass


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date = models.DateTimeField('date created', default=datetime.now())
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=MEDIUM)
    done = models.BooleanField(default=False)
    list = "list"

    class Meta:
        ordering = ('priority',)

    pass


class Tag(models.Model):
    pass
