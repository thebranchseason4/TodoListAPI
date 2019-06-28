from django.db import models


class TodoList(models.Model):
    pass


class Task(models.Model):
    pass


class Tag(models.Model):
    text = models.CharField(max_length=15)
    task = models.ManyToManyField(Task, related_name='tags')
