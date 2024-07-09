from django.urls import path
from .views import AttendanceListView, TakeAttendanceView

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance-list'),
    path('take/<int:class_id>/', TakeAttendanceView.as_view(), name='take-attendance'),
]
