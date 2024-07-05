from django.db import models
from django.contrib.auth.models import User
from datetime import date


class ClassName(models.Model):
    BOOK_CHOICES = [
        ('qaidah', 'Qaidah'),
        ('quran_reading', 'Quran Reading'),
        ('hifz', 'Hifz'),
        ('na', 'N/A'),
    ]

    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True,
                                limit_choices_to={'user_type__in': ['admin_teacher', 'regular_teacher']})
    book = models.CharField(max_length=20, choices=BOOK_CHOICES, default='na')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin_teacher', 'Admin Teacher'),
        ('regular_teacher', 'Regular Teacher'),
        ('student', 'Student'),
        ('waiting_list', 'Waiting List'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='waiting_list')
    class_name = models.ForeignKey(ClassName, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    attendance = models.FloatField(default=0.0, null=True, blank=True)
    punctuality = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reason = models.CharField(max_length=255, null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taken_attendances')

    class Meta:
        unique_together = ('student', 'class_name', 'date')

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.status} on {self.date}"
