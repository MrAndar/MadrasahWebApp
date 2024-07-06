from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, ClassName
from .forms import ExtendedUserCreationForm, ClassForm


def error_404_view(request, exception):
    return render(request, 'accounts/404.html', status=404)


def error_403_view(request, exception):
    return render(request, 'accounts/403.html', status=403)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'


class ProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ExtendedUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile-list')

    def test_func(self):
        return self.request.user.profile.user_type == 'admin_teacher'


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'accounts/profiles_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = Profile.objects.all()
        user_type = self.request.GET.get('user_type', None)
        search_query = self.request.GET.get('search', None)

        if user_type:
            queryset = queryset.filter(user_type=user_type)

        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(class_name__name__icontains=search_query) |
                Q(user_type__icontains=search_query)
            )

        return queryset


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['user_type', 'class_name', 'attendance', 'punctuality']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile-list')

    def test_func(self):
        # Allow only admin teachers to update profiles
        return self.request.user.profile.user_type == 'admin_teacher'


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile_confirm_delete.html'
    success_url = reverse_lazy('profile-list')

    def test_func(self):
        # Allow only admin teachers to delete profiles
        return self.request.user.profile.user_type == 'admin_teacher'


class ClassListView(LoginRequiredMixin, ListView):
    model = ClassName
    template_name = 'accounts/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        queryset = ClassName.objects.all()
        search_query = self.request.GET.get('search', None)
        book_filter = self.request.GET.get('book', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(teacher__user__first_name__icontains=search_query) |
                Q(teacher__user__last_name__icontains=search_query)
            )

        if book_filter:
            queryset = queryset.filter(book=book_filter)

        return queryset


class ClassDetailView(LoginRequiredMixin, DetailView):
    model = ClassName
    template_name = 'accounts/class_detail.html'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.get_object()
        students = Profile.objects.filter(class_name=class_obj)
        context['students'] = students
        return context


class ClassCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClassName
    form_class = ClassForm
    template_name = 'accounts/class_form.html'
    success_url = reverse_lazy('class-list')

    def test_func(self):
        return self.request.user.profile.user_type == 'admin_teacher'


class ClassUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClassName
    form_class = ClassForm
    template_name = 'accounts/class_form.html'
    success_url = reverse_lazy('class-list')

    def test_func(self):
        return self.request.user.profile.user_type == 'admin_teacher'


class ClassDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClassName
    template_name = 'accounts/class_confirm_delete.html'
    success_url = reverse_lazy('class-list')

    def test_func(self):
        return self.request.user.profile.user_type == 'admin_teacher'

