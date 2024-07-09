from django import forms
from django.forms import formset_factory

from accounts.models import Profile
from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['status', 'reason']
        widgets = {
            'status': forms.Select(choices=[
                ('P', 'Present'),
                ('L', 'Late'),
                ('A', 'Absent')
            ]),
            'reason': forms.TextInput(attrs={'placeholder': 'Reason if late or absent'})
        }


AttendanceFormSet = formset_factory(AttendanceForm, extra=0)
