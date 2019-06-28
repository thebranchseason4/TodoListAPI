from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL


class TodoList(models.Model):
    owner = models.ForeignKey(User, on_delete=SET_NULL, related_name='lists', null=True)
    list_name = models.CharField(max_length=255, default="")
    creation_date = models.DateTimeField('date_created', default=datetime.now())


class Task(models.Model):
    pass


class Tag(models.Model):
    pass
