from django import forms
from django.contrib.auth.models import User
from .models import Student

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        password = forms.CharField(widget=forms.PasswordInput)
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # change this to specific fields when the project is more developed
        exclude = ['user']  # Exclude the user field since it will be set automatically based on the logged-in user


