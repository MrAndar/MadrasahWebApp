# daily_readings/forms.py

from django import forms
from .models import DailyReading


class DailyReadingForm(forms.ModelForm):
    class Meta:
        model = DailyReading
        fields = ['date', 'completed']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data['date']
        if DailyReading.objects.filter(student=self.student, date=date).exists():
            raise forms.ValidationError("You have already completed the daily reading for this date.")
        return date
