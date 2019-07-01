from datetime import datetime

from rest_framework import status, serializers
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from .models import *
from .serializers import *


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
        data = {'creation_date': date, 'list_name': 'test1', }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(TodoList.objects.first().creation_date.replace(tzinfo=None), date)
        self.assertEqual(TodoList.objects.first().list_name, 'test1')
        self.assertEqual(TodoList.objects.first().owner, None)


class TagsTests(APITestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(title="test task", description="Desc of test task", date=datetime.now(),
                                          priority=HIGH)
        self.task_2 = Task.objects.create(title="test task 2", description="Desc of test task 2", date=datetime.now(),
                                          priority=LOW)

    def test_create_tag(self):
        url = reverse('tag-list')
        data = {'text': 'test tag', 'task': [self.task_1.pk, ]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().text, 'test tag')

    def test_get_tags(self):
        Tag.objects.create(text="test get tag")
        Tag.objects.create(text="test get tag 2")
        url = reverse('tag-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_tag(self):
        tag_1 = Tag.objects.create(text="test get tag")
        tag_1.task.add(self.task_1)
        url = reverse('tag-detail', args=(tag_1.pk,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': tag_1.pk, 'text': "test get tag", 'task': [self.task_1.pk, ]})

    def test_put_tag(self):
        test_tag = Tag.objects.create(text="test tag")
        test_tag.task.add(self.task_1)
        url = reverse('tag-detail', args=(test_tag.pk,))
        data = {'text': 'new test put tag', 'task': [self.task_2.pk, ]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': test_tag.pk, 'text': "new test put tag", 'task': [self.task_2.pk, ]})

