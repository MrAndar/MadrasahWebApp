# attendance/views.py
from datetime import date

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from .models import Attendance
from .forms import AttendanceForm, AttendanceFormSet
from accounts.models import Profile, ClassName


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendance_records'

    def get_queryset(self):
        user_profile = self.request.user.profile
        if user_profile.user_type == 'admin_teacher':
            return Attendance.objects.all().order_by('-date')
        elif user_profile.user_type == 'regular_teacher':
            return Attendance.objects.filter(profile__class_name__teacher=user_profile).order_by('-date')
        else:
            return Attendance.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendance_records = self.get_queryset().select_related('profile', 'profile__class_name')

        classes = {}
        for record in attendance_records:
            class_name = record.profile.class_name
            if class_name not in classes:
                classes[class_name] = {}
            if record.profile not in classes[class_name]:
                classes[class_name][record.profile] = []
            classes[class_name][record.profile].append(record)

        context['classes'] = classes
        return context


class AttendanceDetailView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_detail.html'
    context_object_name = 'attendance_records'

    def get_queryset(self):
        user_profile = self.request.user.profile
        if user_profile.user_type == 'admin_teacher':
            return Attendance.objects.filter(profile__id=self.kwargs['profile_id']).order_by('-date')
        elif user_profile.user_type == 'regular_teacher':
            return Attendance.objects.filter(profile__id=self.kwargs['profile_id'],
                                             profile__class_name__teacher=user_profile).order_by('-date')
        else:
            return Attendance.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
        attendance_records = self.get_queryset()

        present_count = attendance_records.filter(status='P').count()
        absent_count = attendance_records.filter(status='A').count()
        late_count = attendance_records.filter(status='L').count()

        # Calculate total possible attendances
        user_created_date = profile.user.date_joined.date()
        today = date.today()
        total_possible_attendances = (today - user_created_date).days

        total_attendance_count = present_count + late_count
        if total_possible_attendances > 0:
            attendance_percentage = (total_attendance_count / total_possible_attendances) * 100
            punctuality_percentage = (late_count / (present_count + late_count)) * 100
        else:
            attendance_percentage = 0
            punctuality_percentage = 0

        context['profile'] = profile
        context['present_count'] = present_count
        context['absent_count'] = absent_count
        context['late_count'] = late_count
        context['total_possible_attendances'] = total_possible_attendances
        context['attendance_percentage'] = attendance_percentage
        context['punctuality_percentage'] = punctuality_percentage

        return context


class TakeAttendanceView(LoginRequiredMixin, View):
    template_name = 'attendance/take_attendance.html'
    success_url = reverse_lazy('attendance-list')

    def get(self, request, *args, **kwargs):
        class_instance = get_object_or_404(ClassName, id=self.kwargs['class_id'])
        students = Profile.objects.filter(class_name=class_instance, user_type='student')

        initial_data = [
            {'status': '', 'reason': '', 'profile': student.id}
            for student in students
        ]
        formset = AttendanceFormSet(initial=initial_data)

        form_student_pairs = list(zip(formset.forms, students))

        return render(request, self.template_name,
                      {'formset': formset, 'class_instance': class_instance, 'form_student_pairs': form_student_pairs})

    def post(self, request, *args, **kwargs):
        class_instance = get_object_or_404(ClassName, id=self.kwargs['class_id'])
        students = Profile.objects.filter(class_name=class_instance, user_type='student')
        formset = AttendanceFormSet(request.POST)

        if formset.is_valid():
            for form, student in zip(formset.forms, students):
                if form.is_valid():
                    attendance = form.save(commit=False)
                    attendance.profile = student
                    attendance.date = request.POST['date']
                    attendance.save()
            return redirect(self.success_url)

        form_student_pairs = list(zip(formset.forms, students))

        return render(request, self.template_name,
                      {'formset': formset, 'class_instance': class_instance, 'form_student_pairs': form_student_pairs})


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    fields = ['date', 'status', 'reason']
    template_name = 'attendance/attendance_form.html'

    def get_success_url(self):
        return reverse_lazy('attendance-detail', kwargs={'profile_id': self.object.profile.id})


class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'attendance/attendance_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('attendance-detail', kwargs={'profile_id': self.object.profile.id})
