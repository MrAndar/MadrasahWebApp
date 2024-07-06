from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ClassName


class ClassForm(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = '__all__'


class ExtendedUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('admin_teacher', 'Admin Teacher'),
        ('regular_teacher', 'Regular Teacher'),
        ('student', 'Student'),
        ('waiting_list', 'Waiting List'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'input'}))
    class_name = forms.ModelChoiceField(queryset=ClassName.objects.all(), required=False,
                                        widget=forms.Select(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = self.cleaned_data['user_type']
            profile.class_name = self.cleaned_data['class_name']
            profile.save()

        return user
