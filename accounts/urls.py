from django.urls import path
from .views import (
    HomePageView,
    ProfileListView, ProfileDetailView, ProfileCreateView,
    ClassListView, ClassCreateView, ClassDetailView, AttendanceFormView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='home'),

    path('classes/', ClassListView.as_view(), name='class-list'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),
    path('classes/<int:class_id>/attendance/', AttendanceFormView.as_view(), name='attendance-form'),
    path('classes/new/', ClassCreateView.as_view(), name='class-create'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),

    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/create/', ProfileCreateView.as_view(), name='profile-create'),
]
