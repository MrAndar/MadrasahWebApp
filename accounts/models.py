from django.db import models
from django.contrib.auth.models import User


class ClassName(models.Model):
    QAIDAH = 'qaidah'
    QURAN_READING = 'quran_reading'
    HIFZ = 'hifz'
    NA = 'na'

    BOOK_CHOICES = [
        (QAIDAH, 'Qaidah'),
        (QURAN_READING, 'Quran Reading'),
        (HIFZ, 'Hifz'),
        (NA, 'N/A'),
    ]

    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        'Profile',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'user_type__in': ['admin_teacher', 'regular_teacher']}
    )
    book = models.CharField(max_length=20, choices=BOOK_CHOICES, default=NA)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"


class Profile(models.Model):
    ADMIN_TEACHER = 'admin_teacher'
    REGULAR_TEACHER = 'regular_teacher'
    STUDENT = 'student'
    WAITING_LIST = 'waiting_list'

    USER_TYPE_CHOICES = [
        (ADMIN_TEACHER, 'Admin Teacher'),
        (REGULAR_TEACHER, 'Regular Teacher'),
        (STUDENT, 'Student'),
        (WAITING_LIST, 'Waiting List'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=WAITING_LIST)
    class_name = models.ForeignKey(
        ClassName,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    attendance = models.FloatField(default=0.0, null=True, blank=True)
    punctuality = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
