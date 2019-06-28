from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from .models import *


class TaskModelTest(TestCase):

    def test_task_created_with_proper_title_and_description(self):
        task = Task(title="Play Rust", description="Play Rust after work")
        self.assertEquals(task.title, "Play Rust")
        self.assertEquals(task.description, "Play Rust after work")

    def test_task_high_priority(self):
        task = Task(priority=HIGH)
        other_task = Task(priority=4)
        self.assertEquals(task.priority, HIGH)
        self.assertEquals(other_task.priority, HIGH)

    def test_task_ordering(self):
        first = Task(priority=TOP)
        first.save()
        third = Task(priority=MEDIUM)
        third.save()
        second = Task(priority=HIGH)
        second.save()
        fifth = Task(priority=VERY_LOW)
        fifth.save()
        fourth = Task(priority=LOW)
        fourth.save()

        ordered = [first, second, third, fourth, fifth]
        tasks = list(Task.objects.all())
        self.assertEquals(tasks, ordered)


class TodoListTestCase(APITestCase):
    def test_create_todo_list(self):
        """
        Ensure we can create a new TodoList object.
        """
        date = datetime.now()
        url = reverse('todolist-list')
        data = {'date_created': date, 'list_name': 'test1', }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(TodoList.objects.first().creation_date.replace(tzinfo=None), date)
        self.assertEqual(TodoList.objects.first().list_name, 'test1')
        self.assertEqual(TodoList.objects.first().owner, None)