from django.db import models
from format_checker import RestrictedFileField, RestrictedImageField


class Post(models.Model):
    FULL = 'FL'
    PART = 'PT'
    CONTRACT = 'CT'
    TEMPORARY = 'TY'
    COMMISSION = 'CN'
    INTERNSHIP = 'IN'

    JOB_TYPE_CHOICES = (
        (FULL, 'Full-time'),
        (PART, 'Part-time'),
        (CONTRACT, 'Contract'),
        (TEMPORARY, 'Temporary'),
        (COMMISSION, 'Commission'),
        (INTERNSHIP, 'Internship'),
    )

    title = models.CharField(max_length=80)
    company = models.ForeignKey('Company')
    description = models.TextField()
    date = models.DateField()

    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=30, default="Owatonna, MN")
    low_salary = models.IntegerField()
    high_salary = models.IntegerField()

    def __unicode__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=80)
    picture = RestrictedImageField()
    description = models.TextField()
    website = models.URLField()
    location = models.CharField(max_length=30, default="Owatonna, MN")

    def __unicode__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField('Post')
    resume = RestrictedFileField(content_types=['application/pdf'])

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80)
    posts = models.ManyToManyField('Post')
    
    def __unicode__(self):
        return self.name