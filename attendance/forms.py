from django import forms
from django.forms import formset_factory

from accounts.models import Profile
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Attendance
        fields = ['status', 'reason']
        widgets = {
            'reason': forms.TextInput(attrs={'placeholder': 'Reason if late or absent'})
        }


AttendanceFormSet = formset_factory(AttendanceForm, extra=0)
