from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from .models import Company
from email_user.models import EmailUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email', 'maxlength': '100'}))

    class Meta:
        model = EmailUser
        fields = ('email', 'password')

    def save(self, commit=True):
        # Save the password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CompanyForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Company Name', 'maxlength': '60'}))

    class Meta:
        model = Company
        fields = ('name',)


class CompanyUpdateForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=TinyMCE(attrs={'class':'form-control', 'rows':'28', 'placeholder': 'Enter Company Description'}))
    website = forms.URLField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'Website URL', 'maxlength': '200'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Location, Ex: Owatonna, MN', 'maxlength': '200'}))
    picture = forms.ImageField(required=False)

    def clean_picture(self):
        picture = self.cleaned_data.get('picture', False)
        if picture:
            if picture._size > 1*1024*1024:
                raise ValidationError("Picture is larger than max (1 mb), please try again.")
            else:
                return picture

    class Meta:
        model = Company
        fields = ('description', 'picture', 'website', 'location')