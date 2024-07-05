from django.urls import path
from .views import (
    HomePageView,
    ProfileListView, ProfileDetailView, ProfileCreateView,
    ClassListView, ClassCreateView, ClassDetailView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('classes/', ClassListView.as_view(), name='class-list'),
    path('classes/new/', ClassCreateView.as_view(), name='class-create'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),

    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/create/', ProfileCreateView.as_view(), name='profile-create'),
]
