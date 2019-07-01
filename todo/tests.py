from datetime import datetime
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import *
from .serializers import *


class TaskModelTest(APITestCase):

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

    def test_task_with_list(self):
        user = User(first_name='Name', last_name='Last Name')
        list = TodoList(list_name='test', owner=user)
        task1 = Task(title='test1', list=list)
        task2 = Task(title='test2', list=list)
        self.assertEquals(task1.list, list)
        self.assertEquals(task2.list, list)

    def test_task_with_response(self):
        user = User(first_name='Name', last_name='Last Name')
        user.save()
        list = TodoList(list_name='test', owner=user)
        list.save()
        date = datetime.now()
        url = reverse('task-list')
        data = {'title': 'test', 'description': 'this is a test', 'date': date, 'list': list.id}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().date.replace(tzinfo=None), date)
        self.assertEqual(Task.objects.first().title, 'test')
        self.assertEqual(Task.objects.first().description, 'this is a test')
        self.assertEqual(Task.objects.first().list, list)



class TodoListTestCase(APITestCase):
    def test_create_todo_list(self):
        """
        Ensure we can create a new TodoList object.
        """
        date = datetime.now()
        url = reverse('todolist-list')
        data = {'creation_date': date, 'list_name': 'test1', }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(TodoList.objects.first().creation_date.replace(tzinfo=None), date)
        self.assertEqual(TodoList.objects.first().list_name, 'test1')
        self.assertEqual(TodoList.objects.first().owner, None)