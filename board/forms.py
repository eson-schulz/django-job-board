from django import forms
from .models import Post, Category
import datetime


class PostForm(forms.ModelForm):

    CATEGORY_CHOICES = [[x.id, x.name] for x in Category.objects.all()]

    title = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Enter Job Title'}))
    # Company not generated by user
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'6', 'placeholder': 'Enter Job Description'}))
    # Date is hidden to the user
    date = forms.DateField(initial=datetime.date.today, widget=forms.HiddenInput)

    location = forms.CharField(max_length=30, initial="Owatonna, MN", widget=forms.TextInput(attrs={'type': 'text', 'class':'form-control', 'placeholder': 'Enter Location'}))
    job_type = forms.ChoiceField(choices=Post.JOB_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    low_salary = forms.IntegerField(min_value=5, max_value=10000000, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Salary Ex: 40000'}))
    high_salary = forms.IntegerField(min_value=6, max_value=10000000, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Salary Ex: 50000'}))

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.order_by('name'), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Post
        exclude = ['company']