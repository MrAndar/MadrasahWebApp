from django.urls import path
from .views import (AttendanceListView, AttendanceDetailView,
                    TakeAttendanceView, AttendanceUpdateView, AttendanceDeleteView)

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance-list'),
    path('take/<int:class_id>/', TakeAttendanceView.as_view(), name='take-attendance'),
    path('detail/<int:profile_id>/', AttendanceDetailView.as_view(), name='attendance-detail'),
    path('update/<int:pk>/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('delete/<int:pk>/', AttendanceDeleteView.as_view(), name='attendance-delete'),

]
