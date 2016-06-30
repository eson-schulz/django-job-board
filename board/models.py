from django.db import models
from django.template.defaultfilters import slugify
from account.models import Company
import itertools


class Post(models.Model):
    HOURLY = "HR"
    DAILY = "DA"
    WEEKLY = "WK"
    MONTHLY = "MO"
    YEARLY = "YR"

    SALARY_TYPE_CHOICES = (
        (HOURLY, 'Hourly'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    )

    title = models.CharField(max_length=60)
    company = models.ForeignKey(Company)
    description = models.TextField()
    date = models.DateField()

    job_type = models.ForeignKey('JobType')
    location = models.CharField(max_length=30, default="Owatonna, MN")

    low_salary = models.IntegerField(blank=True, null=True)
    high_salary = models.IntegerField(blank=True, null=True)
    type_salary = models.CharField(max_length=2, choices=SALARY_TYPE_CHOICES, blank=True, null=True)

    # Used for dealing with purchases
    paid = models.BooleanField(default=False)

    # Used for an admin to verify posts to make sure they are OK
    verified = models.BooleanField(default=False)

    # Instructions for application
    application_details = models.CharField(max_length=600, blank=True, null=True)

    # The address posts are sent to (if blank, sends to original email address)
    email = models.EmailField()

    slug = models.SlugField(unique=True)

    categories = models.ManyToManyField('Category')

    def save(self, *args, **kwargs):

        if not self.id:
            max_length = 50

            self.slug = orig = slugify(self.title)[:max_length]

            for x in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def post_count(self):
        return len(self.post_set.all())

    def save(self, *args, **kwargs):

        if not self.id:
            max_length = 80

            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Category.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class JobType(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def post_count(self):
        return len(self.post_set.all())

    def save(self, *args, **kwargs):
        if not self.id:
            max_length = 80

            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not JobType.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(JobType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField('Post')
    resume = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return self.name