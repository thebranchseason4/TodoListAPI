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

    def test_get_todo_list(self):
        user = User.objects.create(username='jouse', email="email@email.com", password='password')
        user2 = User.objects.create(username='jose', email="email@email.com", password='password')
        date = datetime.now()
        url = reverse('todolist-list')
        TodoList.objects.create(owner=user, date_created=date, list_name='test1')
        TodoList.objects.create(owner=user2, date_created=date, list_name='test2')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TodoList.objects.count(), 2)
        self.assertEqual(TodoList.objects.first().owner, user)
        self.assertEqual(TodoList.objects.last().owner, user2)

    def test_put_todo_list(self):
        user = User.objects.create(username='jouse', email="email@email.com", password='password')
        date = datetime.now()
        list= TodoList.objects.create(owner=user, date_created=date, list_name='test1')
        url = reverse('todolist-detail', args=[list.pk, ])
        data = {'owner': 1, 'date_created': date, 'list_name': 'testput', 'tasks': []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(TodoList.objects.first().owner, user)
        self.assertEqual(TodoList.objects.first().list_name, 'testput')

    def test_getone_todo_list(self):
        user = User.objects.create(username='jouse', email="email@email.com", password='password')
        date = datetime.now()
        list1 = TodoList.objects.create(owner=user, date_created=date.replace(tzinfo=None), list_name='testlist1')
        url = reverse('todolist-detail', args=[list1.pk, ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TodoList.objects.first().owner, user)
        self.assertEqual(response.data['owner'], user.pk)
        self.assertEqual(response.data['id'], list1.pk)
        self.assertEqual(response.data['list_name'], 'testlist1')


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test-user', password='test1234', email='test@user.com')

    def test_api_create_user(self):
        url = reverse('user-list')
        data = {'username': 'username', 'password': 'test1234', 'email': 'test@user.com'}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_api_get_user(self):
        url = reverse('user-detail', args=(1, ))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], self.user.username)
        self.assertEquals(response.data['lists'], [])

    def test_api_update_user(self):
        url = reverse('user-detail', args=(1,))

        get_response = self.client.get(url, format='json')
        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(get_response.data['username'], 'test-user')

        data = {'username': 'user', 'password': 'test1234', 'email': 'test@user.com'}
        put_response = self.client.put(url, data, format='json')
        self.assertEquals(put_response.status_code, status.HTTP_200_OK)

        get_response = self.client.get(url, format='json')
        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(get_response.data['username'], 'user')

    def test_api_delete_user(self):
        url = reverse('user-detail', args=(1, ))

        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        get_response = self.client.get(url, format='json')
        self.assertEquals(get_response.status_code, status.HTTP_404_NOT_FOUND)


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
        data = {'text': 'new tag', 'task': [self.task_2.pk, ]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': test_tag.pk, 'text': "new tag", 'task': [self.task_2.pk, ]})