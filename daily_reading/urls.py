# daily_readings/urls.py

from django.urls import path
from .views import DailyReadingListView, DailyReadingCreateView, DailyReadingUpdateView, DailyReadingDeleteView

urlpatterns = [
    path('', DailyReadingListView.as_view(), name='daily_reading_list'),
    path('new/', DailyReadingCreateView.as_view(), name='daily_reading_create'),
    path('<int:pk>/edit/', DailyReadingUpdateView.as_view(), name='daily_reading_update'),
    path('<int:pk>/delete/', DailyReadingDeleteView.as_view(), name='daily_reading_delete'),
]
