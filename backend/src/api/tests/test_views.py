from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from dj_rest_auth.models import TokenModel
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Department, WorkType, Category, Priority, Position, DevType, \
    Device, Ticket


class UserViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='anon', password='!QAZ1qaz')

    def test_list(self):
        url = reverse('user-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'username': 'anon',
            'tickets': [],
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'username': 'anon',
            'tickets': [],
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'password': '@WSX2wsx',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        token = TokenModel.objects.create(user=User.objects.get())
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'password': '@WSX2wsx',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'username': 'testuser',
            'tickets': [],
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class DepartmentViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Department.objects.create(title='Божий дар')

    def test_list(self):
        url = reverse('department-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'Божий дар',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('department-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'Божий дар',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('department-list')
        data = {
            'title': 'НИИ ЧАВО',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('department-list')
        data = {
            'title': 'НИИ ЧАВО',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': 'НИИ ЧАВО',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class WorkTypeViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        WorkType.objects.create(title='Восстановление работоспособности')

    def test_list(self):
        url = reverse('worktype-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'Восстановление работоспособности',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('worktype-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'Восстановление работоспособности',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('worktype-list')
        data = {
            'title': 'Обмотать изолентой',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('worktype-list')
        data = {
            'title': 'Обмотать изолентой',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': 'Обмотать изолентой',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class CategoriesViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='ИВК')

    def test_list(self):
        url = reverse('category-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'ИВК',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'ИВК',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('category-list')
        data = {
            'title': 'ПМО',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('category-list')
        data = {
            'title': 'ПМО',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': 'ПМО',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class PriorityViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Priority.objects.create(number=1, title='Низкий')

    def test_list(self):
        url = reverse('priority-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'number': 1,
            'title': 'Низкий',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('priority-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'number': 1,
            'title': 'Низкий',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('priority-list')
        data = {
            'number': 2,
            'title': 'Нормальный',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('priority-list')
        data = {
            'number': 2,
            'title': 'Нормальный',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'number': 2,
            'title': 'Нормальный',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class PositionViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Position.objects.create(title='Синяя изолента', quantity=10)

    def test_list(self):
        url = reverse('position-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'Синяя изолента',
            'quantity': 10,
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('position-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'Синяя изолента',
            'quantity': 10,
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('position-list')
        data = {
            'title': 'HP226X',
            'quantity': 15,
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('position-list')
        data = {
            'title': 'HP226X',
            'quantity': 15,
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': 'HP226X',
            'quantity': 15,
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class DevTypeViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        DevType.objects.create(title='АРМ')

    def test_list(self):
        url = reverse('devtype-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'АРМ',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('devtype-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': 'АРМ',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('devtype-list')
        data = {
            'title': 'ПМО',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('devtype-list')
        data = {
            'title': 'ПМО',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': 'ПМО',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class DeviceViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        department = Department.objects.create(title='Божий дар')
        dev_type = DevType.objects.create(title='АРМ')
        Device.objects.create(inv_num='510100034', title='Dell Inspiron 7577',
                              department=department, type=dev_type)

    def test_list(self):
        url = reverse('device-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('device-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('device-list')
        data = {
            'inv_num': '136000764',
            'title': 'Microsoft Surface',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('device-list')
        data = {
            'inv_num': '136000764',
            'title': 'Microsoft Surface',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'inv_num': '136000764',
            'title': 'Microsoft Surface',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())

    def test_title_filtering(self):
        url = reverse('device-list')
        res_empty = self.client.get(url, {'title_like': 'No such device'})
        res_found = self.client.get(url, {'title_like': '7577'})
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_department_filtering(self):
        url = reverse('device-list')
        res_empty = self.client.get(url, {'department': 'No such department'})
        res_found = self.client.get(url, {'department': 'Божий дар'})
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_type_filtering(self):
        url = reverse('device-list')
        res_empty = self.client.get(url, {'type': 'No such type'})
        res_found = self.client.get(url, {'type': 'АРМ'})
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_inv_num_filtering(self):
        url = reverse('device-list')
        res_empty = self.client.get(url, {'inventory_like': 'No such i_no'})
        res_found = self.client.get(url, {'inventory_like': '51'})
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_sorting(self):
        department = Department.objects.get()
        dev_type = DevType.objects.get()
        Device.objects.create(inv_num='340756', title='Microsoft Surface',
                              type=dev_type, department=department)
        url = reverse('device-list')
        res_id_asc = self.client.get(url, {'order': 'asc', 'sort': 'id'})
        res_id_desc = self.client.get(url, {'order': 'desc', 'sort': 'id'})
        expected_data1 = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        expected_data2 = {
            'id': 2,
            'inv_num': '340756',
            'title': 'Microsoft Surface',
            'department': 'Божий дар',
            'type': 'АРМ',
        }
        self.assertEqual(res_id_asc.json()[0], expected_data1)
        self.assertEqual(res_id_desc.json()[0], expected_data2)


class TicketViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        owner = User.objects.create(username='anon', password='!QAZ1qaz')
        department = Department.objects.create(title='Божий дар')
        work_done = WorkType.objects.create(title='Восстановление работоспособности')
        priority = Priority.objects.create(number=1, title='Низкий')
        category = Category.objects.create(title='ИВК')
        dev_type = DevType.objects.create(title='АРМ')
        device = Device.objects.create(inv_num='510100034', title='Dell Inspiron 7577',
                                       department=department, type=dev_type)
        ticket = Ticket.objects.create(created=date.today(), owner=owner, priority=priority,
                              device=device, category=category,
                              description='Не работает клавиша Shift')
        ticket.work_done.add(work_done)
        ticket.save()

    def test_list(self):
        url = reverse('ticket-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('ticket-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('ticket-list')
        data = {
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Вышел из строя НЖМД',
            'device': {
                'inv_num': '510100034',
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'detail': 'Authentication credentials were not provided.',
        }
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json(), expected_data)

    def test_create_authorized(self):
        user = User.objects.get()
        token = TokenModel.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('ticket-list')
        data = {
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Вышел из строя НЖМД',
            'device': {
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Вышел из строя НЖМД',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())

    def test_department_filtering(self):
        url = reverse('ticket-list')
        res_empty = self.client.get(url, {'department': 'No such department'})
        res_found = self.client.get(url, {'department': 'Божий дар'})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_inv_num_filtering(self):
        url = reverse('ticket-list')
        res_empty = self.client.get(url, {'inventory_like': 'No such i_no'})
        res_found = self.client.get(url, {'inventory_like': '51'})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_description_filtering(self):
        url = reverse('ticket-list')
        res_empty = self.client.get(url, {'description_like': 'No such description'})
        res_found = self.client.get(url, {'description_like': 'клавиша'})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_status_filtering(self):
        url = reverse('ticket-list')
        res_empty = self.client.get(url, {'status': 0})
        res_found = self.client.get(url, {'status': 1})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_date_lte_filtering(self):
        url = reverse('ticket-list')
        datestamp = date.today() - timedelta(days=2)
        res_empty = self.client.get(url, {'date_lte': datestamp.strftime('%Y-%m-%dT%H:%M:%S')})
        res_found = self.client.get(url, {'date_lte': date.today().strftime('%Y-%m-%dT%H:%M:%S')})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_date_gte_filtering(self):
        url = reverse('ticket-list')
        datestamp = date.today() + timedelta(days=2)
        res_empty = self.client.get(url, {'date_gte': datestamp.strftime('%Y-%m-%dT%H:%M:%S')})
        res_found = self.client.get(url, {'date_gte': date.today().strftime('%Y-%m-%dT%H:%M:%S')})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_sorting(self):
        owner = User.objects.get()
        work_done = WorkType.objects.get()
        priority = Priority.objects.get()
        category = Category.objects.get()
        device = Device.objects.get()
        ticket = Ticket.objects.create(created=date.today(), owner=owner, priority=priority,
                                       device=device, category=category,
                                       description='Вышел из строя НЖМД')
        ticket.work_done.add(work_done)
        ticket.save()
        url = reverse('ticket-list')
        res_id_asc = self.client.get(url, {'order': 'asc', 'sort': 'id'})
        res_id_desc = self.client.get(url, {'order': 'desc', 'sort': 'id'})
        expected_data1 = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Не работает клавиша Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        expected_data2 = {
            'id': 2,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': 'Вышел из строя НЖМД',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': 'Божий дар',
                'type': 'АРМ'
            },
            'work_done': ['Восстановление работоспособности'],
            'priority': 'Низкий',
            'expenditures': [],
            'category': 'ИВК',
            'status': True
        }
        self.assertEqual(res_id_asc.json()[0], expected_data1)
        self.assertEqual(res_id_desc.json()[0], expected_data2)










