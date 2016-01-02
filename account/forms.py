from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from .models import Company


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email', 'maxlength': '254'}))

    class Meta:
        model = User
        fields = ('email', 'password')


class CompanyForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Company Name', 'maxlength': '60'}))

    class Meta:
        model = Company
        fields = ('name',)


class CompanyUpdateForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=TinyMCE(attrs={'class':'form-control', 'rows':'28', 'placeholder': 'Enter Company Description'}))
    website = forms.URLField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'Website URL', 'maxlength': '200'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Location, Ex: Owatonna, MN', 'maxlength': '200'}))

    class Meta:
        model = Company
        fields = ('description', 'picture', 'website', 'location')