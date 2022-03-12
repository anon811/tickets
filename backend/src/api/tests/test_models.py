from django.test import TestCase
from api.models import Priority, WorkType, Category, DevType, Department, Position, Device, \
                        Ticket
from django.contrib.auth.models import User


class PriorityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Priority.objects.create(number=1, title='Низкий')

    def setUp(self):
        self.priority = Priority.objects.get(id=1)

    def test_number_field_label(self):
        field_label = self.priority._meta.get_field('number').verbose_name
        self.assertEqual(field_label, 'Номер')

    def test_title_field_label(self):
        field_label = self.priority._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Приоритет')

    def test_title_max_length(self):
        max_length = self.priority._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_object_name(self):
        expected_name = self.priority.title
        self.assertEqual(expected_name, str(self.priority))

    def test_verbose_name(self):
        v_name = self.priority._meta.verbose_name
        self.assertEqual(v_name, 'Приоритет')

    def test_verbose_name_plural(self):
        v_name_plural = self.priority._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Приоритеты')


class WorkTypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        WorkType.objects.create(title='Ремонт')

    def setUp(self):
        self.w_type = WorkType.objects.get(id=1)

    def test_title_field_label(self):
        field_label = self.w_type._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Тип работ')

    def test_title_max_length(self):
        max_length = self.w_type._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_name(self):
        expected_name = self.w_type.title
        self.assertEqual(expected_name, str(self.w_type))

    def test_verbose_name(self):
        v_name = self.w_type._meta.verbose_name
        self.assertEqual(v_name, 'Тип выполняемых работ')

    def test_verbose_name_plural(self):
        v_name_plural = self.w_type._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Типы выполняемых работ')


class CategoryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='ИВК')

    def setUp(self):
        self.category = Category.objects.get(id=1)

    def test_title_field_label(self):
        field_label = self.category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Категория')

    def test_title_max_length(self):
        max_length = self.category._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_object_name(self):
        expected_name = self.category.title
        self.assertEqual(expected_name, str(self.category))

    def test_verbose_name(self):
        v_name = self.category._meta.verbose_name
        self.assertEqual(v_name, 'Категория заявки')

    def test_verbose_name_plural(self):
        v_name_plural = self.category._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Категории заявок')


class DevTypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        DevType.objects.create(title='АРМ')

    def setUp(self):
        self.dev_type = DevType.objects.get(id=1)

    def test_title_field_label(self):
        field_label = self.dev_type._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Тип устройства')

    def test_title_max_length(self):
        max_length = self.dev_type._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_object_name(self):
        expected_name = self.dev_type.title
        self.assertEqual(expected_name, str(self.dev_type))

    def test_verbose_name(self):
        v_name = self.dev_type._meta.verbose_name
        self.assertEqual(v_name, 'Тип устройства/оборудования')

    def test_verbose_name_plural(self):
        v_name_plural = self.dev_type._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Типы устройств/оборудования')


class DepartmentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Department.objects.create(title='Божий дар')

    def setUp(self):
        self.department = Department.objects.get(id=1)

    def test_title_field_label(self):
        field_label = self.department._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Организация')

    def test_title_max_length(self):
        max_length = self.department._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_name(self):
        expected_name = self.department.title
        self.assertEqual(expected_name, str(self.department))

    def test_verbose_name(self):
        v_name = self.department._meta.verbose_name
        self.assertEqual(v_name, 'Организация')

    def test_verbose_name_plural(self):
        v_name_plural = self.department._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Организации')


class PositionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Position.objects.create(title='Синяя изолента', quantity='10')

    def setUp(self):
        self.position = Position.objects.get(id=1)

    def test_quantity_field_label(self):
        field_label = self.position._meta.get_field('quantity').verbose_name
        self.assertEqual(field_label, 'Количество, шт.')

    def test_title_field_label(self):
        field_label = self.position._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Наименование позиции')

    def test_title_max_length(self):
        max_length = self.position._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_object_name(self):
        expected_name = self.position.title
        self.assertEqual(expected_name, str(self.position))

    def test_verbose_name(self):
        v_name = self.position._meta.verbose_name
        self.assertEqual(v_name, 'Позиция')

    def test_verbose_name_plural(self):
        v_name_plural = self.position._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Позиции (склад)')


class DeviceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        department = Department.objects.create(title='Божий дар')
        type = DevType.objects.create(title='АРМ')
        Device.objects.create(inv_num='510100034', title='Dell Inspiron 7577',
                              department=department, type=type)

    def setUp(self):
        self.device = Device.objects.get(id=1)

    def test_inv_num_field_label(self):
        field_label = self.device._meta.get_field('inv_num').verbose_name
        self.assertEqual(field_label, 'Инвентарный/сер. номер')

    def test_title_field_label(self):
        field_label = self.device._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название устр.')

    def test_inv_num_max_length(self):
        max_length = self.device._meta.get_field('inv_num').max_length
        self.assertEqual(max_length, 30)

    def test_title_max_length(self):
        max_length = self.device._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_department_field_label(self):
        field_label = self.device._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'Организация')

    def test_type_field_label(self):
        field_label = self.device._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'Тип устр.')

    def test_object_name(self):
        expected_name = self.device.title
        self.assertEqual(expected_name, str(self.device))

    def test_verbose_name(self):
        v_name = self.device._meta.verbose_name
        self.assertEqual(v_name, 'Устройство/оборудование')

    def test_verbose_name_plural(self):
        v_name_plural = self.device._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Устройства/оборудование')


class TicketTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='anon', password='!QAZ1qaz')
        department = Department.objects.create(title='Божий дар')
        priority = Priority.objects.create(number=1, title='Низкий')
        category = Category.objects.create(title='ИВК')
        dev_type = DevType.objects.create(title='АРМ')
        device = Device.objects.create(type=dev_type, title='Dell Inspiron 7577',
                                       department=department, inv_num='510100034')
        Ticket.objects.create(owner=user, description='Все пропало!', priority=priority,
                              category=category, device=device)

    def setUp(self):
        self.ticket = Ticket.objects.get(id=1)

    def test_created_field_label(self):
        field_label = self.ticket._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'Дата создания')

    def test_closed_field_label(self):
        field_label = self.ticket._meta.get_field('closed').verbose_name
        self.assertEqual(field_label, 'Дата закрытия')

    def test_owner_field_label(self):
        field_label = self.ticket._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'Исполнитель')

    def test_description_field_label(self):
        field_label = self.ticket._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Описание')

    def test_device_field_label(self):
        field_label = self.ticket._meta.get_field('device').verbose_name
        self.assertEqual(field_label, 'Устройство')

    def test_work_done_field_label(self):
        field_label = self.ticket._meta.get_field('work_done').verbose_name
        self.assertEqual(field_label, 'Выполненные работы')

    def test_priority_field_label(self):
        field_label = self.ticket._meta.get_field('priority').verbose_name
        self.assertEqual(field_label, 'Приоритет')

    def test_category_field_label(self):
        field_label = self.ticket._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'Категория')

    def test_status_field_label(self):
        field_label = self.ticket._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Статус')

    def test_object_name(self):
        expected_name = f'Заявка №{self.ticket.id}'
        self.assertEqual(expected_name, str(self.ticket))

    def test_verbose_name(self):
        v_name = self.ticket._meta.verbose_name
        self.assertEqual(v_name, 'Заявка')

    def test_verbose_name_plural(self):
        v_name_plural = self.ticket._meta.verbose_name_plural
        self.assertEqual(v_name_plural, 'Заявки')