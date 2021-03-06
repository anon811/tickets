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
        Department.objects.create(title='?????????? ??????')

    def test_list(self):
        url = reverse('department-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '?????????? ??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('department-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '?????????? ??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('department-list')
        data = {
            'title': '?????? ????????',
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
            'title': '?????? ????????',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': '?????? ????????',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class WorkTypeViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        WorkType.objects.create(title='???????????????????????????? ??????????????????????????????????')

    def test_list(self):
        url = reverse('worktype-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '???????????????????????????? ??????????????????????????????????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('worktype-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '???????????????????????????? ??????????????????????????????????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('worktype-list')
        data = {
            'title': '???????????????? ??????????????????',
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
            'title': '???????????????? ??????????????????',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': '???????????????? ??????????????????',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class CategoriesViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='??????')

    def test_list(self):
        url = reverse('category-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('category-list')
        data = {
            'title': '??????',
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
            'title': '??????',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class PriorityViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Priority.objects.create(number=1, title='????????????')

    def test_list(self):
        url = reverse('priority-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'number': 1,
            'title': '????????????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('priority-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'number': 1,
            'title': '????????????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('priority-list')
        data = {
            'number': 2,
            'title': '????????????????????',
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
            'title': '????????????????????',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'number': 2,
            'title': '????????????????????',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class PositionViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Position.objects.create(title='?????????? ????????????????', quantity=10)

    def test_list(self):
        url = reverse('position-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '?????????? ????????????????',
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
            'title': '?????????? ????????????????',
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

        DevType.objects.create(title='??????')

    def test_list(self):
        url = reverse('devtype-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0], expected_data)

    def test_detail(self):
        url = reverse('devtype-detail', kwargs={'pk': 1})
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'title': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('devtype-list')
        data = {
            'title': '??????',
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
            'title': '??????',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'title': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())


class DeviceViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        department = Department.objects.create(title='?????????? ??????')
        dev_type = DevType.objects.create(title='??????')
        Device.objects.create(inv_num='510100034', title='Dell Inspiron 7577',
                              department=department, type=dev_type)

    def test_list(self):
        url = reverse('device-list')
        res = self.client.get(url, format='json')
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': '?????????? ??????',
            'type': '??????',
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
            'department': '?????????? ??????',
            'type': '??????',
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_create_not_authorized(self):
        url = reverse('device-list')
        data = {
            'inv_num': '136000764',
            'title': 'Microsoft Surface',
            'department': '?????????? ??????',
            'type': '??????',
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
            'department': '?????????? ??????',
            'type': '??????',
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'inv_num': '136000764',
            'title': 'Microsoft Surface',
            'department': '?????????? ??????',
            'type': '??????',
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
            'department': '?????????? ??????',
            'type': '??????',
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_department_filtering(self):
        url = reverse('device-list')
        res_empty = self.client.get(url, {'department': 'No such department'})
        res_found = self.client.get(url, {'department': '?????????? ??????'})
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': '?????????? ??????',
            'type': '??????',
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_type_filtering(self):
        url = reverse('device-list')
        res_empty = self.client.get(url, {'type': 'No such type'})
        res_found = self.client.get(url, {'type': '??????'})
        expected_data = {
            'id': 1,
            'inv_num': '510100034',
            'title': 'Dell Inspiron 7577',
            'department': '?????????? ??????',
            'type': '??????',
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
            'department': '?????????? ??????',
            'type': '??????',
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
            'department': '?????????? ??????',
            'type': '??????',
        }
        expected_data2 = {
            'id': 2,
            'inv_num': '340756',
            'title': 'Microsoft Surface',
            'department': '?????????? ??????',
            'type': '??????',
        }
        self.assertEqual(res_id_asc.json()[0], expected_data1)
        self.assertEqual(res_id_desc.json()[0], expected_data2)


class TicketViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        owner = User.objects.create(username='anon', password='!QAZ1qaz')
        department = Department.objects.create(title='?????????? ??????')
        work_done = WorkType.objects.create(title='???????????????????????????? ??????????????????????????????????')
        priority = Priority.objects.create(number=1, title='????????????')
        category = Category.objects.create(title='??????')
        dev_type = DevType.objects.create(title='??????')
        device = Device.objects.create(inv_num='510100034', title='Dell Inspiron 7577',
                                       department=department, type=dev_type)
        ticket = Ticket.objects.create(created=date.today(), owner=owner, priority=priority,
                              device=device, category=category,
                              description='???? ???????????????? ?????????????? Shift')
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '?????????? ???? ?????????? ????????',
            'device': {
                'inv_num': '510100034',
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '?????????? ???? ?????????? ????????',
            'device': {
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
            'status': True
        }
        res = self.client.post(url, data=data, format='json')
        expected_data = {
            'id': 2,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': '?????????? ???? ?????????? ????????',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
            'status': True
        }
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, res.json())

    def test_department_filtering(self):
        url = reverse('ticket-list')
        res_empty = self.client.get(url, {'department': 'No such department'})
        res_found = self.client.get(url, {'department': '?????????? ??????'})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
            'status': True
        }
        self.assertEqual(len(res_empty.json()), 0)
        self.assertEqual(res_found.json()[0], expected_data)

    def test_description_filtering(self):
        url = reverse('ticket-list')
        res_empty = self.client.get(url, {'description_like': 'No such description'})
        res_found = self.client.get(url, {'description_like': '??????????????'})
        expected_data = {
            'id': 1,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
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
                                       description='?????????? ???? ?????????? ????????')
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
            'description': '???? ???????????????? ?????????????? Shift',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
            'status': True
        }
        expected_data2 = {
            'id': 2,
            'created': '2022-02-20',
            'closed': None,
            'owner': 'anon',
            'description': '?????????? ???? ?????????? ????????',
            'device': {
                'id': 1,
                'inv_num': '510100034',
                'title': 'Dell Inspiron 7577',
                'department': '?????????? ??????',
                'type': '??????'
            },
            'work_done': ['???????????????????????????? ??????????????????????????????????'],
            'priority': '????????????',
            'expenditures': [],
            'category': '??????',
            'status': True
        }
        self.assertEqual(res_id_asc.json()[0], expected_data1)
        self.assertEqual(res_id_desc.json()[0], expected_data2)










