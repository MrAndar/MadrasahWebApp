from django.urls import path
from .views import (
    HomePageView,
    ProfileListView, ProfileDetailView, ProfileCreateView, ProfileUpdateView, ProfileDeleteView,
    ClassListView, ClassCreateView, ClassDetailView, ClassUpdateView, ClassDeleteView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='home'),

    path('classes/', ClassListView.as_view(), name='class-list'),
    path('classes/new/', ClassCreateView.as_view(), name='class-create'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),
    path('classes/<int:pk>/update/', ClassUpdateView.as_view(), name='class-update'),
    path('classes/<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),

    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('profiles/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profiles/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]
