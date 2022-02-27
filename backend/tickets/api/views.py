from datetime import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Ticket, WorkType, Category, Priority, Position, Device, Expenditure, Department, DevType
from .serializers import TicketSerializer, UserSerializer, WorkTypeSerializer, CategorySerializer,\
    PrioritySerializer, PositionSerializer, DeviceSerializer, ExpenditureSerializer, DepartmentSerializer,\
    DevTypeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        dt_exclude = ['', 'undefined']

        filter_params = {}

        orders = {
            'asc': '',
            'desc': '-'
        }

        dt_format = '%Y-%m-%dT%H:%M:%S'

        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        order = self.request.query_params.get('order', '')
        sort = self.request.query_params.get('sort', '')

        date_lte = self.request.query_params.get('date_lte', '').split('.')[0]
        date_gte = self.request.query_params.get('date_gte', '').split('.')[0]

        status = self.request.query_params.get('status', '')

        department = self.request.query_params.get('department', '')

        inv_num = self.request.query_params.get('inventory_like', '')
        description = self.request.query_params.get('description_like', '')

        if inv_num:
            filter_params['device__inv_num__startswith'] = inv_num

        if description:
            filter_params['description__icontains'] = description

        if status in ('1', '0'):
            filter_params['status'] = status

        if department and department != 'Любая':
            filter_params['device__department__title'] = department

        if date_gte not in dt_exclude:
            date_from = datetime.strptime(date_gte, dt_format)
            filter_params['created__gte'] = date_from

        if date_lte not in dt_exclude:
            date_to = datetime.strptime(date_lte, dt_format)
            filter_params['created__lte'] = date_to

        try:
            queryset = self.queryset.filter(**filter_params).order_by()
            if sort and order:
                queryset = queryset.order_by(orders[order] + sort)
            if start and end:
                queryset = queryset[int(start): int(end)]
        except KeyError as err:
            print('Key error:', err)
            queryset = self.queryset
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class WorkTypeViewSet(viewsets.ModelViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get_queryset(self):
        filter_params = {}

        orders = {
            'asc': '',
            'desc': '-'
        }

        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        order = self.request.query_params.get('order', '')
        sort = self.request.query_params.get('sort', '')

        title = self.request.query_params.get('contains', '')

        if title:
            filter_params['title__icontains'] = title

        try:
            queryset = self.queryset.filter(**filter_params)

            if sort and order:
                queryset = queryset.order_by(orders[order] + sort)

            if start and end:
                queryset = queryset[int(start): int(end)]
        except KeyError as e:
            print(e)
            queryset = self.queryset

        return queryset


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        filter_params = {}

        orders = {
            'asc': '',
            'desc': '-'
        }

        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        order = self.request.query_params.get('order', '')
        sort = self.request.query_params.get('sort', '')

        inventory_num = self.request.query_params.get('inventory_like', '')
        title = self.request.query_params.get('title_like', '')
        department = self.request.query_params.get('department')
        dev_type = self.request.query_params.get('type')

        if inventory_num:
            filter_params['inv_num__startswith'] = inventory_num

        if title:
            filter_params['title__icontains'] = title

        if department and department != 'Любая':
            filter_params['department__title'] = department

        if dev_type and dev_type != 'Любой':
            filter_params['type__title'] = dev_type

        try:
            queryset = self.queryset.filter(**filter_params)
            if order and sort:
                queryset = queryset.order_by(orders[order] + sort)
            if start and end:
                queryset = queryset[int(start): int(end)]
        except KeyError as e:
            print(e)
            queryset = self.queryset
        return queryset


class DevTypeViewSet(viewsets.ModelViewSet):
    queryset = DevType.objects.all()
    serializer_class = DevTypeSerializer


class ExpenditureViewSet(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer


@api_view(['GET'])
def ticket_per_date(request):
    filter_params = {}
    dt_format = '%Y-%m-%dT%H:%M:%S'
    date_lte = request.query_params.get('date_lte', '').split('.')[0]
    date_gte = request.query_params.get('date_gte', '').split('.')[0]
    date_from = datetime.strptime(date_gte, dt_format)
    date_to = datetime.strptime(date_lte, dt_format)
    status = request.query_params.get('status', '')

    if status in ('1', '0'):
        filter_params['status'] = status

    queryset = Ticket.objects.filter(created__range=[date_from, date_to], **filter_params)\
        .values('created').annotate(count=Count('id'))
    data = dict([(item['created'].strftime("%Y-%m-%d"), item['count']) for item in queryset])
    return Response(data)





