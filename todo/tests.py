from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import *


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

    def test_task_ordering_post_request(self):
        url = reverse('task-list')
        self.client.post(url, {'priority': MEDIUM, 'title': 'third', 'description': 'description'}, format='json')
        self.client.post(url, {'priority': LOW, 'title': 'fouth', 'description': 'description'}, format='json')
        self.client.post(url, {'priority': TOP, 'title': 'first', 'description': 'description'}, format='json')
        self.client.post(url, {'priority': VERY_LOW, 'title': 'fifth', 'description': 'description'}, format='json')
        self.client.post(url, {'priority': HIGH, 'title': 'second', 'description': 'description'}, format='json')
        response = self.client.get(url, format='json')
        tasks = response.data
        tasks_priorities = [task['priority'] for task in tasks]
        self.assertEquals(all([tasks_priorities[i] >= tasks_priorities[i+1] for i in
                               range(len(tasks_priorities)-1)]), True)

    def test_task_with_list(self):
        user = User(first_name='Name', last_name='Last Name')
        list = TodoList(list_name='test', owner=user)
        task1 = Task(title='test1', list=list)
        task2 = Task(title='test2', list=list)
        self.assertEquals(task1.list, list)
        self.assertEquals(task2.list, list)

    def test_task_with_list_api(self):
        user_url = reverse('user-list')
        user_data = {'username': 'username', 'password': 'password', 'email': 'email@domain.com'}
        user_response = self.client.post(user_url, user_data, format='json')
        self.assertEquals(user_response.status_code, status.HTTP_201_CREATED)

        list_url = reverse('todolist-list')
        list_data = {'owner': user_response.data['id'], 'list_name': 'test1'}
        list_response = self.client.post(list_url, list_data, format='json')
        self.assertEquals(list_response.status_code, status.HTTP_201_CREATED)

        task_url = reverse('task-list')
        task_data = {'priority': MEDIUM, 'title': 'third', 'description': 'description', 'list': list_response.data['id']}
        task_response = self.client.post(task_url, task_data, format='json')
        self.assertEquals(task_response.status_code, status.HTTP_201_CREATED)

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
        user = User.objects.create(username='jouse', email="email@email.com", password='password')
        date = datetime.now()
        url = reverse('todolist-list')
        data = {'owner': 1, 'date_created': date, 'list_name': 'test1', 'tasks': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(TodoList.objects.first().date_created.replace(tzinfo=None), date)
        self.assertEqual(TodoList.objects.first().list_name, 'test1')
        self.assertEqual(TodoList.objects.first().owner, user)


class UserTestCase(APITestCase):

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'test-user', 'password': 'test1234', 'email': 'test@user.com'}
        response = self.client.post(url, data, format='json')
        usuario = User.objects.first()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(usuario.username, 'test-user')

    def test_get_user(self):
        user = User.objects.create(username='test-user', password='test1234', email='test@user.com')
        url = reverse('user-detail', args=(1, ))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], user.username)
        self.assertEquals(response.data['lists'], [])
