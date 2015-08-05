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
    company = models.ForeignKey('Company')
    description = models.TextField()
    date = models.DateField()

    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=30, default="Owatonna, MN")

    low_salary = models.IntegerField(blank=True, null=True)
    high_salary = models.IntegerField(blank=True, null=True)
    type_salary = models.CharField(max_length=2, choices=SALARY_TYPE_CHOICES, blank=True, null=True)

    slug = models.SlugField(unique=True)

    categories = models.ManyToManyField('Category', blank=True)

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

    def save(self, *args, **kwargs):

        if not self.id:
            max_length = 50

            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=60)
    picture = models.ImageField(blank=True, upload_to="companies/")
    description = models.TextField()
    website = models.URLField()
    location = models.CharField(max_length=30, default="Owatonna, MN")

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):

        if not self.id:
            max_length = 50

            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField('Post')
    resume = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return self.name