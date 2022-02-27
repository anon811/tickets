from django.db import models


class Ticket(models.Model):
    created = models.DateField(db_index=True, blank=True, null=True,
                               verbose_name='Дата создания')
    closed = models.DateField(blank=True, null=True, db_index=True, verbose_name='Дата закрытия')
    owner = models.ForeignKey('auth.User', related_name='tickets', on_delete=models.PROTECT,
                              verbose_name='Исполнитель')
    description = models.TextField(verbose_name='Описание')
    device = models.ForeignKey('Device', related_name='tickets', on_delete=models.PROTECT,
                               verbose_name='Устройство')
    work_done = models.ManyToManyField('WorkType', related_name='tickets', blank=True,
                                       verbose_name='Выполненные работы')
    priority = models.ForeignKey('Priority', related_name='tickets', blank=True, null=True,
                                 on_delete=models.PROTECT, verbose_name='Приоритет')
    category = models.ForeignKey('Category', related_name='tickets', on_delete=models.PROTECT,
                                 verbose_name='Категория')
    status = models.BooleanField(default=True, verbose_name='Статус')

    def __str__(self):
        return f'Заявка №{self.id}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Priority(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер')
    title = models.CharField(max_length=100, unique=True, verbose_name='Приоритет')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'


class WorkType(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Тип работ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип выполняемых работ'
        verbose_name_plural = 'Типы выполняемых работ'


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория заявки'
        verbose_name_plural = 'Категории заявок'


class Device(models.Model):
    inv_num = models.CharField(max_length=30, db_index=True, unique=True, verbose_name='Инвентарный/сер. номер')
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название устр.')
    department = models.ForeignKey('Department', related_name='devices', on_delete=models.PROTECT,
                                   verbose_name='Организация')
    type = models.ForeignKey('DevType', related_name='devices', on_delete=models.PROTECT,
                             verbose_name='Тип устр.')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Устройство/оборудование'
        verbose_name_plural = 'Устройства/оборудование'


class DevType(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Тип устройства')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип устройства/оборудования'
        verbose_name_plural = 'Типы устройств/оборудования'


class Department(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Организация')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Position(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Наименование позиции')
    quantity = models.PositiveIntegerField(verbose_name='Количество, шт.')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции (склад)'


class Expenditure(models.Model):
    position = models.ForeignKey('Position', related_name='expenditures', on_delete=models.PROTECT,
                                 verbose_name='Позиция (склад)')
    quantity = models.PositiveIntegerField(verbose_name='Расход, шт.')
    ticket = models.ForeignKey('Ticket', blank=True, null=True, related_name='expenditures',
                               on_delete=models.CASCADE, verbose_name='Заявка')

    def save(self, *args, **kwargs):
        self.position.quantity -= self.quantity
        self.position.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.position.quantity += self.quantity
        self.position.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.position.title} : {self.quantity}'

    class Meta:
        verbose_name = 'Расход ЗИП со склада'
        verbose_name_plural = 'Расход ЗИП со склада'