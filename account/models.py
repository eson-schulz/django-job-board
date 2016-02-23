from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import itertools


class Company(models.Model):
    user = models.OneToOneField(User)

    name = models.CharField(max_length=60)
    picture = models.ImageField(blank=True, upload_to="companies/")
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(blank=True, max_length=30, default="Owatonna, MN")

    # Used for Stripe communication
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    slug = models.SlugField(unique=True)

    def post_count(self):
        return len(self.post_set.all())

    def save(self, *args, **kwargs):

        if not self.id:
            max_length = 50

            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Company.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name