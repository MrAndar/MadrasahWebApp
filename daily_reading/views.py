# daily_readings/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import DailyReading
from .forms import DailyReadingForm
from accounts.models import Profile
from datetime import datetime, timedelta


class DailyReadingListView(ListView):
    model = DailyReading
    template_name = 'daily_reading/daily_reading_list.html'
    context_object_name = 'daily_readings'

    def get_queryset(self):
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday() + 1)  # Last Tuesday
        end_date = start_date + timedelta(days=6)  # Sunday of the same week
        return DailyReading.objects.filter(date__range=[start_date, end_date]).order_by('date', 'student')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday() + 1)  # Last Tuesday
        dates = [start_date + timedelta(days=i) for i in range(7)]
        context['dates'] = dates

        # Collect readings per student
        students = Profile.objects.all()
        student_readings = []

        for student in students:
            readings = []
            for date in dates:
                reading = DailyReading.objects.filter(student=student, date=date).first()
                readings.append((date, reading))
            student_readings.append((student, readings))

        context['student_readings'] = student_readings
        return context


class DailyReadingCreateView(LoginRequiredMixin, CreateView):
    model = DailyReading
    form_class = DailyReadingForm
    template_name = 'daily_reading/daily_reading_form.html'
    success_url = reverse_lazy('daily_reading_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.instance.student = self.request.user.profile
        return super().form_valid(form)


class DailyReadingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DailyReading
    form_class = DailyReadingForm
    template_name = 'daily_reading/daily_reading_form.html'
    success_url = reverse_lazy('daily_reading_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.instance.student = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        reading = self.get_object()
        return self.request.user.profile == reading.student or self.request.user.profile.user_type == 'admin_teacher'


class DailyReadingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DailyReading
    template_name = 'daily_reading/daily_reading_confirm_delete.html'
    success_url = reverse_lazy('daily_reading_list')

    def test_func(self):
        reading = self.get_object()
        return self.request.user.profile == reading.student or self.request.user.profile.user_type == 'admin_teacher'
