from django.contrib import admin
from .models import Ticket, Device, Department, DevType, WorkType, Priority, Category, Position, Expenditure

admin.site.register(Ticket)
admin.site.register(Device)
admin.site.register(Department)
admin.site.register(DevType)
admin.site.register(WorkType)
admin.site.register(Priority)
admin.site.register(Category)
admin.site.register(Position)
admin.site.register(Expenditure)