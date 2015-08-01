from django.db import models
from django.template.defaultfilters import slugify
import itertools


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

    title = models.CharField(max_length=60)
    company = models.ForeignKey('Company')
    description = models.TextField()
    date = models.DateField()

    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=30, default="Owatonna, MN")
    low_salary = models.IntegerField(blank=True, null=True)
    high_salary = models.IntegerField(blank=True, null=True)

    slug = models.SlugField(unique=True, max_length=70)

    categories = models.ManyToManyField('Category', blank=True)

    def save(self, *args, **kwargs):

        # TODO: Save the post's slug

        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=60)
    picture = models.ImageField(blank=True, null=True)
    description = models.TextField()
    website = models.URLField()
    location = models.CharField(max_length=30, default="Owatonna, MN")

    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField('Post')
    resume = models.FileField(blank=True, null=True)

    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80)

    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name