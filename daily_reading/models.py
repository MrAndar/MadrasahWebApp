from django.db import models
from accounts.models import Profile  # Assuming Profile is in accounts app


class DailyReading(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='daily_readings')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'date'], name='unique_student_date')
        ]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date}: {'Completed' if self.completed else 'Not Completed'}"
