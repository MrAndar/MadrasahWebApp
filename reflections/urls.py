from django.urls import path
from .views import (
    ReflectionListView, ReflectionDetailView, ReflectionCreateView,
    ReflectionUpdateView, ReflectionDeleteView
)

urlpatterns = [
    path('', ReflectionListView.as_view(), name='reflection-list'),
    path('<int:pk>/', ReflectionDetailView.as_view(), name='reflection-detail'),
    path('new/', ReflectionCreateView.as_view(), name='reflection-create'),
    path('<int:pk>/edit/', ReflectionUpdateView.as_view(), name='reflection-update'),
    path('<int:pk>/delete/', ReflectionDeleteView.as_view(), name='reflection-delete'),
]
