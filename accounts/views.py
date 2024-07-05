from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .models import Profile, ClassName, Attendance
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import ExtendedUserCreationForm, ClassForm, AttendanceForm, AttendanceFormSet


def error_404_view(request, exception):
    return render(request, 'accounts/404.html', status=404)


def error_403_view(request, exception):
    return render(request, 'accounts/403.html', status=403)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'


class ProfileCreateView(LoginRequiredMixin, CreateView):
    form_class = ExtendedUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile-list')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.profile.user_type == 'admin_teacher':
            return self.handle_no_permission()  # Redirect non-admin teachers
        return super().dispatch(*args, **kwargs)


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
                Q(teacher__icontains=search_query)
            )

        if book_filter:
            queryset = queryset.filter(book=book_filter)

        return queryset


class ClassDetailView(DetailView):
    model = ClassName
    template_name = 'accounts/class_detail.html'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.get_object()
        students = Profile.objects.filter(class_name=class_obj)

        # Create empty Attendance instances for each student if not already present for today
        for student in students:
            Attendance.objects.get_or_create(
                student=student.user,
                class_name=class_obj,
                date=date.today(),
                defaults={'status': 'absent', 'teacher': self.request.user}
                # Default status to 'absent' and set the teacher
            )

        attendance_formset = AttendanceFormSet(
            queryset=Attendance.objects.filter(class_name=class_obj, date=date.today())
        )
        context['students'] = students
        context['attendance_formset'] = attendance_formset
        return context


class AttendanceFormView(FormView):
    template_name = 'accounts/class_detail.html'
    form_class = AttendanceFormSet

    def form_valid(self, formset):
        class_id = self.kwargs['class_id']
        class_obj = get_object_or_404(ClassName, id=class_id)
        for form in formset:
            form.instance.class_name = class_obj
            form.instance.teacher = self.request.user
            form.save()
        return redirect('class-detail', pk=class_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = get_object_or_404(ClassName, id=self.kwargs['class_id'])
        context['class'] = class_obj
        context['attendance_formset'] = AttendanceFormSet(
            queryset=Attendance.objects.filter(class_name=class_obj, date=date.today()))
        return context


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = ClassName
    form_class = ClassForm
    template_name = 'accounts/class_form.html'
    success_url = reverse_lazy('class-list')

    def test_func(self):
        return self.request.user.profile.user_type == 'admin_teacher'
