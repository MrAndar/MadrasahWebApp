from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint

from accounts.models import Profile, ClassName


class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=ATTENDANCE_CHOICES)
    reason = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['profile', 'date'], name='unique_attendance_record')
        ]

    def __str__(self):
        return f"{self.profile} on {self.date}: {self.get_status_display()}"
