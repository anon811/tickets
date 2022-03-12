from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, UserViewSet, WorkTypeViewSet, CategoriesViewSet, PriorityViewSet,\
    ticket_per_date, PositionViewSet, DeviceViewSet, ExpenditureViewSet, DepartmentViewSet, DevTypeViewSet


router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'users', UserViewSet)
router.register(r'worktypes', WorkTypeViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'priorities', PriorityViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'expenditures', ExpenditureViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'devtypes', DevTypeViewSet)


urlpatterns = [
    path('api/dashboard/', ticket_per_date),
    path('api/', include(router.urls)),
]