from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, Device, DevType, Department, WorkType, Priority, Category, Position, Expenditure


class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.HyperlinkedRelatedField(many=True, view_name='ticket-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'tickets']


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = ['id', 'title']


class DeviceSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='title', queryset=DevType.objects)
    department = serializers.SlugRelatedField(slug_field='title', queryset=Department.objects)

    class Meta:
        model = Device
        extra_kwargs = {
            'inv_num': {
                'validators': [],
            },
        }
        fields = ['id', 'inv_num', 'title', 'department', 'type']


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['number', 'title']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title', 'quantity']


class ExpenditureSerializer(serializers.ModelSerializer):
    position = serializers.SlugRelatedField(slug_field='title', queryset=Position.objects)

    class Meta:
        model = Expenditure
        fields = ['id', 'position', 'quantity']

    def validate(self, data):
        """
        Prevent negative position quantity in store.
        """
        pos = data['position']
        available = pos.quantity
        required = data['quantity']
        if available < required:
            raise serializers.ValidationError(f'Доступно всего {available} {pos}')
        return data


class TicketSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    priority = serializers.SlugRelatedField(slug_field='title', queryset=Priority.objects)
    category = serializers.SlugRelatedField(slug_field='title', queryset=Category.objects)
    work_done = serializers.SlugRelatedField(slug_field='title', many=True, queryset=WorkType.objects)
    expenditures = ExpenditureSerializer(many=True)

    class Meta:
        model = Ticket
        extra_kwargs = {'device': {'required': False}}
        fields = ['id', 'created', 'closed', 'owner', 'description', 'device',
                  'work_done', 'priority', 'expenditures', 'category', 'status']

    def update(self, instance, validated_data):

        # Ugly, but easy way to prevent unattended expenditure instances. it is better to use sets for defining
        # which instance needs deletion/creation.
        for exp in instance.expenditures.all():
            exp.delete()

        # Regular data
        instance.created = validated_data.get('created', instance.created)
        instance.closed = validated_data.get('closed', instance.closed)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)

        # Nested objects
        validated_data = self.validated_data_to_device_instance(validated_data)
        validated_data = self.validated_data_to_expenditure_instances(validated_data)

        instance.device = validated_data.get('device', instance.device)
        instance.expenditures.set(validated_data.get('expenditures', instance.expenditures))
        instance.owner = validated_data.get('owner', instance.owner)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.work_done.set(validated_data.get('work_done', instance.work_done))
        instance.category = validated_data.get('category', instance.category)

        instance.save()

        return instance

    def create(self, validated_data):

        validated_data = self.validated_data_to_device_instance(validated_data)
        validated_data = self.validated_data_to_expenditure_instances(validated_data)

        expenditures = validated_data.pop('expenditures')
        work_done = validated_data.pop('work_done')

        instance = Ticket(**validated_data)
        instance.save()

        instance.expenditures.set(expenditures)
        instance.work_done.set(work_done)
        return instance

    @staticmethod
    def validated_data_to_device_instance(data):
        device = Device.objects.get(inv_num=data['device']['inv_num'])
        data['device'] = device
        return data

    @staticmethod
    def validated_data_to_expenditure_instances(data):
        expenditures = []

        for exp_data in data['expenditures']:
            serializer = ExpenditureSerializer(data=exp_data)
            serializer.is_valid()
            expenditure = serializer.save()
            expenditures.append(expenditure)
        data['expenditures'] = expenditures
        return data


class DevTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevType
        fields = ['id', 'title']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
