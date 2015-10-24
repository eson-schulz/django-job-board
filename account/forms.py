from django import forms
from django.contrib.auth.models import User
from .models import Company


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'picture', 'description', 'website', 'location')